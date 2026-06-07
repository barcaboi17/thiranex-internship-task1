# ============================================================
#   THIRANEX INTERNSHIP - TASK 1
#   Data Cleaning & Visualization Project
#   Intern: Suraj | ID: THX-JUN0526-1465
# ============================================================

# --- STEP 0: Import Required Libraries ---
import pandas as pd               # For working with data tables
import matplotlib.pyplot as plt   # For creating charts
import seaborn as sns             # For beautiful visualizations
import warnings
warnings.filterwarnings('ignore') # Suppress minor warnings

print("=" * 55)
print("  THIRANEX INTERNSHIP | Task 1: Data Cleaning & Viz")
print("=" * 55)

# ============================================================
# STEP 1: LOAD THE DATASET
# ============================================================
print("\n📂 STEP 1: Loading Dataset...")

df = pd.read_csv("sales_data.csv")

print(f"✅ Dataset loaded successfully!")
print(f"   Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")
print(f"\nFirst 5 rows:")
print(df.head())

# ============================================================
# STEP 2: EXPLORE THE DATA
# ============================================================
print("\n" + "=" * 55)
print("🔍 STEP 2: Exploring the Data")
print("=" * 55)

print("\n📋 Column Names & Data Types:")
print(df.dtypes)

print("\n📊 Basic Statistics:")
print(df.describe())

print("\n❓ Missing Values in each column:")
print(df.isnull().sum())

print(f"\n🔁 Duplicate Rows: {df.duplicated().sum()}")

# ============================================================
# STEP 3: DATA CLEANING
# ============================================================
print("\n" + "=" * 55)
print("🧹 STEP 3: Data Cleaning")
print("=" * 55)

# --- 3a. Remove Duplicates ---
print("\n[1] Removing Duplicate Rows...")
before = len(df)
df = df.drop_duplicates()
after = len(df)
print(f"   Removed {before - after} duplicate row(s). Rows remaining: {after}")

# --- 3b. Handle Missing Values ---
print("\n[2] Handling Missing Values...")

# Fill missing Age with the median age (middle value)
median_age = df['Age'].median()
df['Age'] = df['Age'].fillna(median_age)
print(f"   ✅ 'Age' missing values filled with median: {median_age}")

# Fill missing Gender with 'Unknown'
df['Gender'] = df['Gender'].fillna('Unknown')
print(f"   ✅ 'Gender' missing values filled with 'Unknown'")

# Fill missing Rating with the mean (average) rating
mean_rating = round(df['Rating'].mean(), 2)
df['Rating'] = df['Rating'].fillna(mean_rating)
print(f"   ✅ 'Rating' missing values filled with mean: {mean_rating}")

# --- 3c. Handle Outliers ---
print("\n[3] Handling Outliers...")

# Fix negative Age values (impossible in real life)
invalid_age = df[df['Age'] < 0].shape[0]
df = df[df['Age'] >= 0]
print(f"   ✅ Removed {invalid_age} row(s) with negative Age values")

# Fix extreme Price outliers using IQR method
Q1 = df['Price'].quantile(0.25)
Q3 = df['Price'].quantile(0.75)
IQR = Q3 - Q1
upper_limit = Q3 + 1.5 * IQR
outlier_count = df[df['Price'] > upper_limit].shape[0]
df = df[df['Price'] <= upper_limit]
print(f"   ✅ Removed {outlier_count} row(s) with extreme Price outliers")
print(f"      (Price threshold: ₹{upper_limit:,.0f})")

# --- 3d. Fix Data Types ---
print("\n[4] Converting Data Types...")
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Age'] = df['Age'].astype(int)
print("   ✅ 'Order_Date' converted to datetime")
print("   ✅ 'Age' converted to integer")

print(f"\n✅ Data Cleaning Complete! Clean dataset: {df.shape[0]} rows x {df.shape[1]} columns")

# ============================================================
# STEP 4: FEATURE ENGINEERING (Creating new useful columns)
# ============================================================
print("\n" + "=" * 55)
print("⚙️  STEP 4: Feature Engineering")
print("=" * 55)

df['Month'] = df['Order_Date'].dt.strftime('%b')  # Jan, Feb, Mar...
df['Month_Num'] = df['Order_Date'].dt.month       # 1, 2, 3...
print("   ✅ Added 'Month' column from Order_Date")

# ============================================================
# STEP 5: VISUALIZATIONS
# ============================================================
print("\n" + "=" * 55)
print("📊 STEP 5: Creating Visualizations...")
print("=" * 55)

# Set a clean style for all charts
sns.set_style("whitegrid")
sns.set_palette("husl")

# --- Create a dashboard with multiple charts ---
fig = plt.figure(figsize=(18, 14))
fig.suptitle("Thiranex Internship | Sales Data Dashboard\nIntern: Suraj | THX-JUN0526-1465",
             fontsize=16, fontweight='bold', y=0.98)

# ---- Chart 1: Sales by Category (Bar Chart) ----
ax1 = fig.add_subplot(2, 3, 1)
category_sales = df.groupby('Category')['Total_Sales'].sum().sort_values(ascending=False)
bars = ax1.bar(category_sales.index, category_sales.values,
               color=['#2ecc71', '#3498db', '#e74c3c'])
ax1.set_title('💰 Total Sales by Category', fontweight='bold')
ax1.set_xlabel('Category')
ax1.set_ylabel('Total Sales (₹)')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
# Add value labels on bars
for bar, val in zip(bars, category_sales.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
             f'₹{val/1000:.0f}K', ha='center', va='bottom', fontsize=9, fontweight='bold')

# ---- Chart 2: Gender Distribution (Pie Chart) ----
ax2 = fig.add_subplot(2, 3, 2)
gender_counts = df['Gender'].value_counts()
colors = ['#ff6b9d', '#4ecdc4', '#95a5a6']
wedges, texts, autotexts = ax2.pie(gender_counts.values,
                                    labels=gender_counts.index,
                                    autopct='%1.1f%%',
                                    colors=colors,
                                    startangle=90,
                                    explode=[0.05]*len(gender_counts))
ax2.set_title('👥 Customer Gender Distribution', fontweight='bold')

# ---- Chart 3: Monthly Sales Trend (Line Chart) ----
ax3 = fig.add_subplot(2, 3, 3)
monthly = df.groupby(['Month_Num', 'Month'])['Total_Sales'].sum().reset_index()
monthly = monthly.sort_values('Month_Num')
ax3.plot(monthly['Month'], monthly['Total_Sales'], marker='o',
         linewidth=2.5, color='#e67e22', markersize=8, markerfacecolor='white',
         markeredgewidth=2)
ax3.fill_between(monthly['Month'], monthly['Total_Sales'], alpha=0.1, color='#e67e22')
ax3.set_title('📈 Monthly Sales Trend', fontweight='bold')
ax3.set_xlabel('Month')
ax3.set_ylabel('Total Sales (₹)')
ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))

# ---- Chart 4: Top 5 Cities by Sales (Horizontal Bar) ----
ax4 = fig.add_subplot(2, 3, 4)
city_sales = df.groupby('City')['Total_Sales'].sum().nlargest(5)
colors_city = sns.color_palette("viridis", len(city_sales))
bars4 = ax4.barh(city_sales.index, city_sales.values, color=colors_city)
ax4.set_title('🏙️ Top 5 Cities by Sales', fontweight='bold')
ax4.set_xlabel('Total Sales (₹)')
ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1000:.0f}K'))
for bar, val in zip(bars4, city_sales.values):
    ax4.text(val + 200, bar.get_y() + bar.get_height()/2,
             f'₹{val/1000:.0f}K', va='center', fontsize=9)

# ---- Chart 5: Rating Distribution (Histogram) ----
ax5 = fig.add_subplot(2, 3, 5)
ax5.hist(df['Rating'], bins=10, color='#9b59b6', edgecolor='white', linewidth=0.8)
ax5.set_title('⭐ Customer Rating Distribution', fontweight='bold')
ax5.set_xlabel('Rating')
ax5.set_ylabel('Number of Orders')
ax5.axvline(df['Rating'].mean(), color='red', linestyle='--',
            linewidth=1.5, label=f"Mean: {df['Rating'].mean():.2f}")
ax5.legend()

# ---- Chart 6: Category vs Avg Rating (Box Plot) ----
ax6 = fig.add_subplot(2, 3, 6)
categories = df['Category'].unique()
data_by_category = [df[df['Category'] == cat]['Rating'].values for cat in categories]
bp = ax6.boxplot(data_by_category, labels=categories, patch_artist=True)
colors_box = ['#2ecc71', '#3498db', '#e74c3c']
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax6.set_title('📦 Rating by Product Category', fontweight='bold')
ax6.set_xlabel('Category')
ax6.set_ylabel('Rating')

plt.tight_layout()
plt.savefig("sales_dashboard.png", dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.show()
print("\n✅ Dashboard saved as: sales_dashboard.png")

# ============================================================
# STEP 6: KEY INSIGHTS SUMMARY
# ============================================================
print("\n" + "=" * 55)
print("💡 STEP 6: Key Insights")
print("=" * 55)

top_category = category_sales.idxmax()
top_city = city_sales.idxmax()
top_product = df.groupby('Product')['Total_Sales'].sum().idxmax()
avg_rating = df['Rating'].mean()

print(f"\n  1. 🏆 Top Sales Category : {top_category}")
print(f"  2. 🏙️  Best Performing City: {top_city}")
print(f"  3. 🛒 Best Selling Product: {top_product}")
print(f"  4. ⭐ Average Rating      : {avg_rating:.2f} / 5.0")
print(f"  5. 📦 Total Orders        : {len(df)}")
print(f"  6. 💰 Total Revenue       : ₹{df['Total_Sales'].sum():,.0f}")

print("\n" + "=" * 55)
print("✅ Task 1 Complete! Dashboard saved as sales_dashboard.png")
print("=" * 55)
