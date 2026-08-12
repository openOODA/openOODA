# RFC 0001: Capability-Based Security Model
* **RFC ID**: 0001
* **Author**: openOODA Core Team
* **Status**: Implemented
* **Created**: 2026-07-28

---

## 💡 Feature Overview
Mandates default-deny security where all I/O operations (network, filesystem, system process execution, environment variable access) require explicit capability handles (`&NetCap`, `&FsCap`, `&SysCap`, `&EnvCap`) passed as function arguments.

## 🎯 Motivation & Problem Statement
Prevent supply chain zero-day attacks and prompt injection execution where third-party packages or AI-generated code attempt unauthorized file reading or network requests.

## 📐 Detailed Specification
```ooda
pub fn fetch_user_profile(net: &NetCap, user_id: u64) -> Result[String, String] {
    let url = "https://api.example.com/users/" + user_id.to_string();
    return net.get(url);
}
```

## 🛡️ Security & Capability Impact
Functions lacking capability handles trap statically during `CapabilityChecker::check_program()`.

## 🧪 Testing & Verification Criteria
Verified by `tests/security/07_net_capability.oo`, `tests/security/08_fs_capability.oo`, and `tests/02_security_sandboxing.oo` in `openOODA/qa`.
