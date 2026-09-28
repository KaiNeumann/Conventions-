---
title: Windows Browser Automation
type: reference
tags: [conventions, development, windows, browser-automation, security]
status: draft
created: 2026-09-28
updated: 2026-09-28
---

# Windows Browser Automation

Any project that drives a real browser on Windows - for tests, scraping,
challenge solving, upload automation, or end-to-end checks - can lock the
operator out of their own machine. This chapter covers the failure, how to
prove who caused it, and how to make it structurally impossible.

The short version: Chromium-family browsers contain a feature that probes the
OS account with a blank-password `LogonUser()` call. Each probe is a failed
interactive logon. Ten of them inside ten minutes is a locked account. The
hardening is cheap; the *diagnosis* is the hard part, and diagnosis is where
projects go wrong.

## The hazard *(rule)*

1. Automated browser work **MUST NOT** be able to cause an OS account
   lockout. A full run over many targets - dozens of contexts, retries,
   challenge fallbacks - must not cost the operator their machine.
2. Every browser process the project launches **MUST** carry the hardening
   in [Hardening every lane](#hardening-every-lane-default), including
   processes launched by *test* and *live* harnesses. A live-test lane that
   skips the flags is a production-grade exposure with none of the
   monitoring.
3. Attribution evidence **MUST** distinguish "no lockout events" from "the
   event log could not be read". These are opposite findings and collapsing
   them is a defect, not a shortcut. See
   [Attribution is the hard part](#attribution-is-the-hard-part-rule).

## How the failure presents

The mechanism, in the order a reader meets it:

1. A Chromium-family feature (historically
   `AutofillAiWalletPrivatePasses`, Chromium issue `541310282`) calls
   `LogonUser()` against the current account with a blank password.
2. Windows rejects it and records **Security event 4625** with
   `LogonType = 2` (interactive) and `SubStatus = 0xc000006a` (wrong
   password), `Status = 0xc000006d` (logon failure). The `ProcessName`
   field names the browser binary that attempted it.
3. Repeated attempts are budgeted by the account lockout policy. A common
   workstation setting is **threshold 10, observation window 10 minutes,
   lockout duration 10 minutes**.
4. The tenth failure inside the window trips **Security event 4740** and the
   account is locked for the lockout duration.

The arithmetic is what makes this dangerous for automation. A single
browser process that opens many contexts can produce many probes, and a
fleet run multiplies that by the number of lanes. Nothing about the failure
looks like an attack in the log; it looks like a user typing a wrong
password repeatedly.

Two consequences deserve emphasis:

- **A lockout is not self-announcing.** The app keeps working, the browser
  keeps launching, the uploads keep failing for an unrelated-looking reason.
  The operator discovers the lockout at the login screen.
- **The offending binary is often not yours.** The probe fires in whatever
  Chromium build handles the request. That is frequently the
  *system-installed* browser or an embedded WebView2 runtime host, not the
  browser bundle the project downloaded. See the war story below.

## Attribution is the hard part *(rule)*

The only field that names a culprit is `ProcessName` on the 4625 record, and
the only place that record lives is the Windows Security event log. Reading
that log requires an **elevated process**. Every trap below is a variant of
the same failure: the run looks clean because nothing was read.

1. **An unelevated read throws, it does not return empty.** Without
   elevation the read fails with an access error. Any correlator that
   passes a silencing flag to the query turns that failure into an empty
   result set, which is indistinguishable from "no events happened". Never
   silence that error in a correlator; let it surface.
2. **A catch-all handler that logs once per process is a false negative.**
   A long run emits one soft line at startup and then nothing. The operator
   reads a silent log as a clean run. Emit the "cannot read the log"
   notice loudly, and re-emit it periodically so it cannot be missed in a
   long log.
3. **"Zero events" is a claim, not a result.** Before accepting it, confirm
   the correlator could actually read the log in that run.
4. **Record the absolute binary path per lane.** Correlating only a lane
   label leaves you unable to tell your bundled browser from a system one.
   Both can appear in the same event stream.
5. **Ship an elevated collector as a product artifact.** A long-running app
   is rarely elevated, so it usually cannot gather its own evidence. Provide
   a small script the operator can run as administrator to dump the
   relevant events, the lockout policy, and the recent lane artifacts into
   one file to attach to a bug report.
6. **Redact account names unconditionally.** The account that got locked is
   frequently *not* the account running the script, so comparing the event's
   target name against the current user leaks the real name. Redact every
   account name, including those inside raw event XML.

A practical positive control, worth repeating on any machine under
suspicion: launch the hardened browser once, note the time, and confirm that
no new 4625 appears at that timestamp. A hardening change with a clean
observation is evidence; a hardening change with no observation is not.

## Hardening every lane *(default)*

Every Chromium-family launch should carry:

```
--disable-http-auth
--auth-server-whitelist=
--auth-negotiate-delegate-whitelist=
--disable-features=AutofillAiWalletPrivatePasses
```

The first three stop the browser from answering HTTP auth challenges or
auto-negotiating with Windows credentials on hosted pages. The last disables
the account-probing feature itself.

1. **One shared list, applied at every spawn site.** Put the flags in a
   single exported constant or builder and route all launch sites through
   it - webdriver wrappers, direct Chrome launches, alternate automation
   backends, and test harnesses. A per-call-site copy list is how lanes
   drift apart, and the lane that drifts is the one that locks the account.
2. **`--disable-features` is single-valued.** A later occurrence of the flag
   silently replaces the earlier one rather than adding to it. If any other
   code path adds its own `--disable-features`, it can undo the hardening
   without any error. Keep every disable in one flag, or merge the lists
   deliberately.
3. **Never hand proxy credentials to a browser.** Userinfo in a proxy URL
   makes the browser authenticate at the proxy layer, which is an OS-level
   auth surface. Strip userinfo at the **sink** - at the point the value
   reaches the launch call - not only upstream where producers normalize it.
   Upstream-only normalization is correct until the first caller that
   forgets.
4. **Engine-specific flags must not cross engines.** The flags above are
   Chromium-only; passing them to a Firefox-based lane breaks or
   misconfigures the launch. Gate them on the engine actually being used.
5. **Verify the flags are really applied.** A launch wrapper that accepts
   extra arguments but never forwards them looks correct in review. A test
   that asserts the launch kwargs contain the hardening flags catches this
   without launching anything.

## Machine-level containment *(default)*

Browser hardening addresses the project's own lanes. It cannot reach the
system browser or an embedded runtime that the operator uses independently,
and on a workstation the account lockout policy is often the only real
protection. For a local workstation account whose lockout is caused by a
known vendor browser bug, disabling lockout is a reasonable trade:

```
net accounts /lockoutthreshold:0
```

For shared, managed, or domain-joined machines this is a security decision
and belongs to the administrator, not to a project's conventions.

Additional machine-level steps worth considering:

- Disable the probing feature for the system browser through its policy
  store, so the operator's own browsing is covered too.
- Identify and update or disable the application that hosts the WebView2
  runtime producing the failures. WebView2 host applications keep a profile
  directory under the user profile, which identifies the host and roughly
  when it ran.
- Prefer a bundled browser under the project's own control over a system
  browser, so the hardened flags are guaranteed to apply.

## Debugging playbook

1. Read the policy, so the arithmetic is known rather than guessed:
   `net accounts` gives threshold, lockout duration, and observation window.
2. Dump the events, elevated, over a window that covers the incident:
   ```powershell
   Get-WinEvent -FilterHashtable @{ LogName='Security'; Id=4625,4740,4771; StartTime=(Get-Date).AddDays(-1) }
   ```
3. Read the fields that decide the case, per event:
   - `ProcessName` - the binary that attempted the logon. This is the
     attribution; everything else is supporting detail.
   - `LogonType` - `2` interactive, `3` network, `8` network cleartext,
     `11` cached interactive. Interactive is the signature of the
     blank-password probe.
   - `Status` / `SubStatus` - `0xc000006d` logon failure,
     `0xc000006a` wrong password, `0xc0000064` no such user.
4. **Resolve the full path against what the project actually launches.** A
   path under a system program directory is a browser or runtime host the
   project does not own; a path under the project's own tool directory is
   the project's own lane. This single comparison resolves most incidents.
5. Cluster the events against the policy threshold before concluding
   anything. Individual scattered failures are noise; a run of failures
   inside one observation window is the lockout.
6. Look for the application-side corroboration the run should have left
   behind: network logs, driver logs, and lane records from the incident
   window. **A window with many lockout events and no lane artifacts at all
   points at an uninstrumented lane or at a non-project binary** - it is a
   strong signal, but it is a hypothesis until `ProcessName` confirms it.
7. Do not re-run a full fleet to "reproduce" a suspected lockout. Each
   attempt extends the exposure and can lock the account again.

## War story: a hardening fix that was not the cause

A recurring lockout was traced to a Chromium account-probing feature. The
project hardened the browser lanes it knew about, added a Security-log
correlator, and closed the issue on evidence that a validation run produced
no lockout events.

The lockout returned. Re-investigation found three things that had been
missed:

1. The correlator ran inside an unelevated app, so it could not read the
   Security log at all. The "no events" result was a swallowed access
   error, and the validation had measured nothing. This is the single most
   expensive mistake in the sequence: an unverified evidence pipeline makes
   every later conclusion unverified too.
2. One alternate automation backend had been added after the first fix and
   never received the hardening flags or the proxy normalization, so it ran
   unprotected and, lacking lane instrumentation, left no artifacts.
3. The decisive evidence, once the log was actually read, showed the
   failing binary was the operator's *system-installed* browser and an
   embedded WebView2 host - neither of which the project had ever launched.
   The project's own browser appeared in none of the events.

The hardening work was still correct and worth keeping - the unhardened
backend was a real defect, and it could have caused the same failure. But it
was not the cause. Only the `ProcessName` field established that, and only
after the evidence pipeline was fixed.

The transferable lessons:

- Fix the evidence before trusting it. If a pipeline can report success
  while reading nothing, every conclusion drawn from it is unsupported.
- Absence of your own artifacts is not attribution. "The project did not do
  it" and "the project did it" are both guesses until the log names a
  binary.
- Automated work has a blast radius that scales with the fleet, and the
  machine under test is the operator's actual workstation. Assume any
  unguarded path will eventually be exercised.

## Anti-patterns

- Silencing the access error that reveals the log could not be read.
- Assuming the browser the project launches is the browser in the event.
- Hardening production lanes but leaving live-test lanes unguarded.
- Normalizing proxy credentials only in the producer, never at the sink.
- Shipping the same Chromium-only flags to a Firefox-based lane.
- Declaring a fix validated without confirming the evidence source was
  readable in that run.
- Attaching an unredacted evidence dump to a public bug report.
- Re-running a full automation fleet to reproduce a suspected lockout.
