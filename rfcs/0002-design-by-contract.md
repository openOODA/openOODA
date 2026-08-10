# RFC 0002: Design by Contract & Verify Syntax
* **RFC ID**: 0002
* **Author**: openOODA Core Team
* **Status**: Implemented
* **Created**: 2026-07-28

---

## 💡 Feature Overview
Bakes preconditions (`requires`), postconditions (`ensures`), and co-located `verify` test blocks directly into function syntax as first-class language keywords.

## 📐 Detailed Specification
```ooda
pub fn divide(a: Float, b: Float) -> Float
    requires b != 0.0
    ensures result * b == a
{
    return a / b;
}

verify divide {
    assert_eq!(divide(10.0, 2.0), 5.0);
}
```

## 🧪 Testing & Verification Criteria
Verified by `ooda test` and `tests/contracts/12_requires_precondition.oo` in `openOODA/qa`.
