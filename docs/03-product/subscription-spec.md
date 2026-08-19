> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/03-product/subscription-spec.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-12 — Subscription, Trial and Cancellation

**Status:** Draft
**Version:** 0.1

## 1. Commercial product

- Monthly plan.
- Annual plan.
- The same family access applies unless a future tiering decision changes it.
- One subscription covers authorized adults and children's family profiles.
- The entitlement belongs to the family, even if the purchase has a payer and channel of origin.

## 2. Channels

| Channel | Purchase and management |
|---|---|
| iOS/iPadOS | App Store In-App Purchase and Apple subscription management. |
| Android | Google Play Billing and Subscription Center. |
| Future Web | Stripe Billing + Checkout Sessions; Customer Portal for self-service. |

The backend normalizes receipts and webhooks into a `SubscriptionEntitlement`. It does not attempt to collect payment directly for a purchase managed by another store.

## 3. Pilot

During the pilot there is no charge or commercial trial. Families receive a `pilot entitlement` with date, scope, and administrative revocation. This avoids mixing product evaluation with paid conversion.

## 4. Free trial

- Duration: 7 days.
- Eligibility: once per eligible family/account, each store's rules applying.
- Benefits: full access to features of the plan being tested.
- Conversion: automatic to the chosen plan if it is not canceled, when the channel allows it.
- Before confirming, duration, subsequent price, date of first payment, frequency, automatic renewal and cancellation method are shown in English and Spanish.
- Send an in-product reminder approximately three days before the end when the channel and consent allow it; do not rely solely on store notifications.
- Canceling during the trial prevents the next charge and maintains access until the end of the trial, subject to the behavior of the channel.

## 5. Recommended cancellation policy

1. Visible `Manage subscription` action on Account.
2. Direct link to Apple, Google Play or Stripe according to `billing_source`.
3. No mandatory call, email or conversation.
4. Show exact date when access ends before confirming.
5. Cancellation turns off automatic renewal.
6. Access continues until the end of the current paid or trial period, unless immediate cancellation is required by law or the payment channel.
7. No prorated refund by default; Apple/Google manage their refunds and the website follows published policy and applicable law.
8. Optional reason question after confirming; never blocks.
9. The user can reactivate before the end of the period when the channel supports it.
10. Canceling does not delete family, Learner Models, portfolio or history. Removal is a separate flow.

## 6. Transparency

The paywall shows with equal clarity:

- “7 days free”.
- Actual monthly or annual total price.
- Conversion date.
- Automatic renewal.
- How to cancel.
- What happens with access and data.
- Link to terms and privacy.

Don't use fake timers, hidden closing buttons, annual prices presented only as a monthly payment, or various confusing steps towards accidental purchase.

## 7. Payment failures and grace

- Retain access during the grace period informed by the store/backend.
- Do not stop a session in progress.
- Show status and action to resolve payment only to the adult payer/Owner.
- Revoke entitlement after confirmed expiration, maintaining data according to policy.

## 8. Multi-channel billing and family access

- Provide a localized `Restore purchases` action.
- Link the purchase to the correct Family through an authenticated adult account.
- Avoid two accidental active subscriptions; warn if the family already has an entitlement through another channel.
- The other authorized adults consume the same entitlement without accessing the Owner's payment data.
- Change of payer or channel requires explicit flow to avoid double charging.

## 9. Web implementation with Stripe

When there is a web purchase:

- Use Stripe Billing with Checkout Sessions in subscription mode.
- Use Customer Portal for cancellation, payment method and invoices.
- Process webhooks idempotently.
- Keep restricted keys and secrets out of clients/repository.
- Evaluate taxes and registrations before activating automatic calculation.

## 10. Requirements

- **SUB-001:** The family has a standardized entitlement independent of the payment channel.
- **SUB-002:** The commercial trial lasts seven days and is offered once based on eligibility.
- **SUB-003:** Terms, price, conversion and cancellation are shown before starting.
- **SUB-004:** The application offers direct access to cancel the source channel.
- **SUB-005:** Cancellation stops renewal and retains access until the end of the period unless an applicable exception requires otherwise.
- **SUB-006:** Cancellation and deletion of data are separate flows.
- **SUB-007:** The reason question is subsequent and optional.
- **SUB-008:** The family should not maintain two active subscriptions by accident.
- **SUB-009:** The pilot uses free entitlement separate from the commercial trial.
- **SUB-010:** The paywall and management are localized in English and Spanish.

## 11. Operational references

- [Apple — introductory offers for auto-renewable subscriptions](https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-introductory-offers-for-auto-renewable-subscriptions)
- [Google Play — subscription transparency, trials and cancellation](https://support.google.com/googleplay/android-developer/answer/9900533)
- [Stripe—Customer Portal](https://docs.stripe.com/customer-management)
- [Stripe—subscription trials](https://docs.stripe.com/billing/subscriptions/trials)
- [FTC—Negative Option Rule resources](https://www.ftc.gov/legal-library/browse/rules/negative-option-rule)

These sources can change and must be reviewed before launch. This specification expresses product policy and is not a substitute for legal review.
