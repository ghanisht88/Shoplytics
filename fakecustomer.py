import pandas as pd
import numpy as np

np.random.seed(42)

customers = pd.DataFrame({
    "customer_id": range(1, 501),
    "customer_name": [
        f"Customer_{i}" for i in range(1, 501)
    ],
    "gender": np.random.choice(
        ["Male", "Female"],
        500
    ),
    "age": np.random.randint(18, 60, 500),
    "city": np.random.choice(
        ["Delhi", "Gurgaon", "Mumbai", "Bangalore", "Pune"],
        500
    ),
    "registration_date": pd.date_range(
        start="2024-01-01",
        periods=500,
        freq="D"
    )
})

print(customers.head())