# inf-all-services-auto

### To install the requirements

```
pip install -r requirements.txt
```

### To run the flask app
```
flask run --port 5000
```

### to call api like this
```
http://localhost:5000/startup_india
```
```
<code>
{
  "comp_address": {
    "address1": "address1",
    "address2": "address2",
    "state": "Tamil Nadu",
    "district": "Thanjavur",
    "pincode": "612001"
  },
  "directors": [
    {
      "Name": "Abdur Rahim",
      "Gender": "Male",
      "Address": "Kumbakonam",
      "Mobile_no": "7418306307",
      "Email": "abdurrahim251103@gmail.com"
    },
    {
      "Name": "Abdur Razzak",
      "Gender": "Male",
      "Address": "Thanjavur",
      "Mobile_no": "9363449277",
      "Email": "abdurrazzak251103@gmail.com"
    },
    {
      "Name": "Rajeshwari",
      "Gender": "Female",
      "Address": "Address2",
      "Mobile_no": "9150144434",
      "Email": "rajeshwari@gmail.com"
    }
  ],
  "username": "avinashpurohit11@gmail.com",
  "mobile_no":"9150144434",
  "password": "India@123",
  "website": "https://www.indiafilings.com/",
  "Industry": "AI",
  "Sector": "NLP",
  "Catogries": ["Governments","Online Aggregator","E-commerce","Subscription Commerce"],
  "stage": "Ideation",
  "no_of_emp": "2",
  "aboutcompany": "",
  "who_we_are": "",
  "solution": "",
  "uniqueness": "",
  "Revenue Growth": "",
  "lOGO_file": "base64_code",
  "LOA_file": "base64_code",
  "COI_file": "base64_code",
  "pitchdesk_file": "base64_code"
}
</code>
```
# to call api like this
```
http://localhost:5000/IECODE
```
```
<code>
{
    "username":"abdurrahim251103@gmail.com",
    "password":"India@123"
}
</code>
```



