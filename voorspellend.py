import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator

# Specify the full path to your JSON file
json_file_path = r'C:\Users\Gebruiker\OneDrive - ASG\Documenten\HU\steam.json'

# Load data from JSON file
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract relevant fields
names = []
developers = []
publishers = []
categories = []
owners = []
prices = []

for item in data:
    price = item.get('price')
    if price is not None and float(price) <= 400:  # Filter out games with price higher than 400
        names.append(item['name'])
        developers.append(item['developer'])
        publishers.append(item['publisher'])
        categories.append(item['categories'])
        owners.append(item['owners'])
        prices.append(price)

# Simple function to calculate mean
def mean(values):
    return sum(values) / len(values)

# Function to calculate the coefficients for linear regression
def linear_regression(X, y):
    n = len(X)
    x_mean = mean(X)
    y_mean = mean(y)

    # Calculate the coefficients
    numerator = sum((X[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((X[i] - x_mean) ** 2 for i in range(n))

    # Check for zero denominator
    if denominator == 0:
        raise ValueError("Denominator in linear regression calculation is zero. Check for variation in the data.")

    b1 = numerator / denominator
    b0 = y_mean - b1 * x_mean

    return b0, b1

# Prepare data for regression
X = []
for owner in owners:
    # Handle ranges like '0 - 20000'
    if ' - ' in owner:
        lower_bound = int(owner.split(' - ')[0])
        X.append(lower_bound)
    else:
        X.append(int(owner.replace(',', '')))  # Convert owners to integers

# Convert prices to float for regression
y = [float(price) for price in prices]  # Ensure prices are in float format

# Calculate coefficients
try:
    b0, b1 = linear_regression(X, y)
except ValueError as e:
    print(e)
    exit()

# Function to make predictions
def predict(x):
    return b0 + b1 * x

# Example predictions
predictions = []
for owner in owners:
    if ' - ' in owner:
        lower_bound = int(owner.split(' - ')[0])
        predictions.append(predict(lower_bound))
    else:
        predictions.append(predict(int(owner.replace(',', ''))))

# Display predictions alongside actual prices
# for i in range(len(prices)):
#     actual_price = float(prices[i])  # Ensure we are comparing as float
#     if actual_price == 0.0:
#         print(f"Actual Price: Free, Predicted Price: {predictions[i]}")
#     else:
#         print(f"Actual Price: {actual_price:.2f}, Predicted Price: {predictions[i]:.2f}")

# Find the top 5 most popular games
# Create a list of tuples (name, owners, price) for sorting
games_data = list(zip(names, owners, prices))

# Sort by number of owners (popularity)
most_popular_games = sorted(games_data, key=lambda x: int(x[1].split(' - ')[0]) if ' - ' in x[1] else int(x[1].replace(',', '')), reverse=True)[:5]

# Sort by price (expensiveness)
most_expensive_games = sorted(games_data, key=lambda x: float(x[2]), reverse=True)[:5]

# Print top 5 most popular games with predicted prices
print("\nTop 5 Most Popular Games:")
for game in most_popular_games:
    # Get the number of owners for prediction
    if ' - ' in game[1]:
        lower_bound = int(game[1].split(' - ')[0])
        predicted_price = predict(lower_bound)
    else:
        predicted_price = predict(int(game[1].replace(',', '')))

    price_display = "Free" if float(game[2]) == 0.0 else game[2]
    print(f"Name: {game[0]}, Owners: {game[1]}, Actual Price: {price_display}, Price by AI: {predicted_price:.2f}")

# Print top 5 most expensive games with predicted prices
print("\nTop 5 Most Expensive Games:")
for game in most_expensive_games:
    # Get the number of owners for prediction
    if ' - ' in game[1]:
        lower_bound = int(game[1].split(' - ')[0])
        predicted_price = predict(lower_bound)
    else:
        predicted_price = predict(int(game[1].replace(',', '')))

    price_display = "Free" if float(game[2]) == 0.0 else game[2]
    print(f"Name: {game[0]}, Owners: {game[1]}, Actual Price: {price_display}, Price by AI: {predicted_price:.2f}")

# Plotting the results
plt.figure(figsize=(13,  5))
plt.scatter(X, y, color='blue', label='Actual Prices', s=30)  # Scatter plot for actual prices
plt.plot(X, predictions, color='red', label='Predicted Prices', linewidth=1.5)  # Regression line
plt.title('Predicted Prices Based on Number of Owners')
plt.xlabel('Number of Owners')
plt.ylabel('Prices')
plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))  # Format x-axis to display numbers
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, nbins=12))  # Set number of ticks on x-axis
plt.legend()
plt.grid()
plt.show()

print("\nPrice by AI is based on the calculation, y= b_0 + b_1·x, with use of linear regression.")