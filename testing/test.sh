#!/bin/bash

# Install jq and faker if not already installed
# sudo apt-get install jq -y
# pip install faker

# Generate random data using faker and bash utilities
generate_random_data() {
    local username=$(python3 -c "from faker import Faker; fake = Faker(); print(fake.user_name())")
    local email=$(python3 -c "from faker import Faker; fake = Faker(); print(fake.email())")
    local phone=$(python3 -c "import random; print(''.join(random.choices('0123456789', k=9)))")
    local city=$(python3 -c "from faker import Faker; fake = Faker(); print(fake.city())")
    local address=$(python3 -c "from faker import Faker; fake = Faker(); print(fake.address())")
    local password=$(python3 -c "from faker import Faker; fake = Faker(); print(fake.password())")

    # Construct JSON payload
    json_payload=$(jq -n \
        --arg username "$username" \
        --arg email "$email" \
        --arg phone "$phone" \
        --arg city "$city" \
        --arg address "$address" \
        --arg password "$password" \
        '{
            user_full_name: $username,
            user_given_name: $username,
            user_email: $email,
            user_phone: $phone,
            user_city: $city,
            user_address: $address,
            user_password: $password
        }')

    # Make the curl PUT request
    curl -X PUT "http://localhost:5000/api/login" \
        -H "Content-Type: application/json" \
        -d "$json_payload"
}

# Execute the function
generate_random_data