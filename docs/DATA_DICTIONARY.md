# Data dictionary

All data is synthetic and generated with seed 42. `legacy.csv` uses source-system formats; `new_sys.csv` uses target-system formats.

| Column | Meaning | Rule |
|---|---|---|
| `loan_id` | Loan key | `L000001` format; unique in legacy |
| `customer_id` | Synthetic customer key | No real customer data |
| `product` | Loan product | Personal, Auto, Mortgage, LOC |
| `region` | Operating region | GTA, East, West, North, Atlantic |
| `origination_date` | Loan start date | `DD/MM/YYYY` in legacy, `YYYY-MM-DD` in target |
| `principal` | Original principal | Positive currency amount |
| `interest_rate` | Annual interest rate | Percent; target defects may be null |
| `status` | Loan lifecycle status | Legacy codes A/D/C/W; target labels |
| `outstanding_balance` | Current balance | Zero for closed/written-off accounts |
