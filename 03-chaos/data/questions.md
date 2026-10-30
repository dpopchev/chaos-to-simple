# Red cards: the questions the story raised

Each one is a bit nobody had written down. The answer that closed it is in
`data/rules.csv` (the What) or in `05-how/s05_how/ports.py` (the How).

1. What if the coupon expired yesterday? -> b0, `coupon.is_valid_on(today)`
2. Does the member discount stack with the coupon, and in which order? -> b1, after the coupon
3. Is the free-shipping threshold checked before or after the discounts? -> b2, after the discount (the planted bug)
   - Marketing: before the discount -- a feature, more customers qualify.
   - Logistics: after the discount -- free shipping is paid from the margin of the discounted goods.
   - Nobody decided it; the code decided for them (incident I2).
   - Decided in the room: after the discount. Who decided: the room (marketing, logistics, the developer).
   - It became the b2 row of `data/rules.csv`: "Shipping is free when the discounted goods come to 50 BGN or more".
4. What happens when the payment is declined? -> s0, `Charged | Declined`
5. What happens when the stock is gone after we priced the order? -> s1, `Reserved | OutOfStock`
6. What happens when the confirmation email bounces? -> s2, `Sent | Bounced`

Still open, for a Friday post: releasing a reservation when the payment is declined
(compensation adds bits to the shell, not to the core).
