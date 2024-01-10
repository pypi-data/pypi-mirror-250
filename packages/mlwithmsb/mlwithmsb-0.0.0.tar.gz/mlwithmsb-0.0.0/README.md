**mlwithmsb: A Versatile Python Package for Outlier Handling in Data Analysis**

Effortlessly clean your datasets and ensure data quality with Outlier Cleaner! This user-friendly package empowers you to detect and address outliers using multiple effective methods, tailored to your specific needs.

**Key Features:**

- **Flexible Outlier Detection:** Choose from IQR, Z-score, or visual inspection methods to identify outliers based on statistical principles or your expert judgment.
- **Customizable Thresholds:** Fine-tune the sensitivity of outlier detection to match your dataset's characteristics and analysis goals.
- **Visual Exploration:** Leverage informative histograms and box plots to visualize data distribution and guide outlier identification in the visual method.
- **Streamlined NaN Handling:** Automatically remove rows containing missing values to maintain data integrity.
- **Easy Integration:** Seamlessly incorporate outlier cleaning into your data analysis workflows with a simple function call.

**Benefits:**

- Improve data quality and accuracy for reliable analysis outcomes.
- Gain deeper insights into your data by identifying and addressing potential anomalies.
- Enhance model performance by mitigating the impact of outliers.
- Foster reproducibility and transparency in your data analysis processes.

**Installation:**

```bash
pip install mlwithmsb
```

**Usage:**

```python
import pandas as pd
from mlwithmsb import remove_outliers

# Load your dataset
data = pd.read_csv("your_data.csv")

# Clean the data using your preferred method and threshold
cleaned_data = remove_outliers(data, method="iqr", threshold=1.5)  # Example



**Embrace robust data cleaning for accurate and reliable insights—install mlwithmsb today!**

