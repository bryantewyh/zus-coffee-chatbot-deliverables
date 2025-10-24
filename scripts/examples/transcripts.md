
# ZUS Coffee API - Real Transcripts

Generated: 2025-10-23 19:25:50


These are real API responses captured from the running server.



## Products Endpoint (`/products`)


### Success Cases


### Example 1: Search for Mugs

**Request:**

```
GET /products?query=mug&top_k=3
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "mug",
  "products": [
    {
      "name": "Stainless Steel Mug | 420ml",
      "category": "Mugs",
      "price": "RM59.00",
      "description": "Coffee smells better outdoors.Does it? I guess it's time to find out! Made for those who cherish the outdoors or simply just prefer sipping their coffee through a mug. Made from durable 304 stainless steel, features double-wall vacuum insulation to keep your drinks hot or cold up to 5 hours.No matter where your journey takes you—whether it’s a roadside coffee break to \"heal\" or a moment in the mountains surrounded by good company—we’re more than just a mug for great coffee. We’re the small comfort you can always count on, wherever the road may lead.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/396.png?v=1738069660&width=1080",
      "url": "https://shop.zuscoffee.com/products/zus-stainless-steel-mug-420ml?_pos=6&_fid=a8ffe8a86&_ss=c"
    },
    {
      "name": "OG Ceramic Mug | 470ml",
      "category": "Mugs",
      "price": "RM19.50",
      "description": "Minimalist mug for delicious sips.Our OG Ceramic Mug makes those small moments all the more comfortable. High-quality ceramic blends effortlessly with an ergonomic handle for an easy grip—ensuring you get the ultimate cosy experience with style and practicality.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/Discount_Badge.png?v=1750817172&width=168",
      "url": "https://shop.zuscoffee.com/products/zus-og-ceramic-mug-470ml?_pos=9&_fid=a8ffe8a86&_ss=c"
    },
    {
      "name": "[Corak Malaysia] Cup Sleeve",
      "category": "Drinkware Accessories",
      "price": "RM39.00",
      "description": "Effortlessly carry your drinks in style.Add a touch of beautiful Malaysian heritage to your drinks with our Cup Sleeve! Made from durable synthetic leather and featuring an adjustable strap that adapts to various cup sizes, it perfectly combines culture with functionality. Plus, it comes with an interchangeable nylon string so you can personalise your look and make it yours.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/New-badge.svg?v=1752712225",
      "url": "https://shop.zuscoffee.com/products/zus-corak-malaysia-cup-sleeve?_pos=8&_fid=a8ffe8a86&_ss=c"
    }
  ],
  "count": 3,
  "top_k": 3
}
```


**Status:** Success - Found 3 product(s)


---



### Example 2: Search for Tumblers

**Request:**

```
GET /products?query=tumbler&top_k=5
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "tumbler",
  "products": [
    {
      "name": "All Day Lid",
      "category": "Drinkware Accessories",
      "price": "RM25.00",
      "description": "This isn’t just a spare part.Have a new tumbler every day with different tops for your favorite bottom! You asked for it, and we heard you loud and clear. Versatile your hydration today!",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/103_e3372861-657d-425c-a330-0cccaecb925d.png?v=1753601893&width=1080",
      "url": "https://shop.zuscoffee.com/products/zus-all-day-cup-500ml-17oz-accessories-lid-demo?_pos=1&_fid=a8ffe8a86&_ss=c"
    },
    {
      "name": "All Day Cup | 500ml",
      "category": "Tumbler",
      "price": "from RM55.30",
      "description": "Your drinks All Day, everyday.This tumbler’s more than a way to sip on delicious drinks. With a leak proof, dual-purpose lid, your hot or iced drinks will be kept perfectly preserved for up to 16 hours so youcanenjoy each sip like it’s the first.Pair your All Day Cup with gorgeous accessories for a colourful upgrade.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/Discount_Badge.png?v=1750817172&width=168",
      "url": "https://shop.zuscoffee.com/products/all-day-cup-500ml-17oz?_pos=11&_fid=a8ffe8a86&_ss=c"
    },
    {
      "name": "All Day Cup Aqua | 500ml",
      "category": "Tumbler",
      "price": "RM79.00",
      "description": "Your drinks All Day, everyday.When you’re the life of the party, you’ll find yourself gravitating towards experiences that can be shared with others. You’re like the endless water: expansive, an adventure waiting to unfold. You’re never in one place when there’s a whole world out there.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/DesignYourOwn-badge.svg?v=1753188579",
      "url": "https://shop.zuscoffee.com/products/all-day-cup-500ml-17oz-aqua-collection?_pos=3&_fid=a8ffe8a86&_ss=c"
    },
    {
      "name": "[Corak Malaysia] Reusable Straw Kit",
      "category": "Drinkware Accessories",
      "price": "RM16.90",
      "description": "Bye-bye single-use straws and hello to sustainable style with the ZUS Reusable Straw Kit! Compact, collapsible, and designed with a carabiner clip, it’s easy to carry wherever you go. Made from food-grade stainless steel with a soft silicone tip to protect your lips and teeth, it’s safe, durable, and simple to clean with the included brush.Whether at home or on the move, the ZUS Reusable Straw Kit keeps every sip convenient and hassle-free.Celebrate local heritage with three stunning new Corak Malaysia designs—available now.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/62_b565f01c-8f6a-487c-bb5f-241958f9b7ff.png?v=1746778301&width=1080",
      "url": "https://shop.zuscoffee.com/products/zus-corak-malaysia-reusable-straw-kit?_pos=4&_fid=a8ffe8a86&_ss=c"
    },
    {
      "name": "Reusable Straw Kit",
      "category": "Drinkware Accessories",
      "price": "RM16.90",
      "description": "Sustainable, convenient sips.Say goodbye to single-use straws with our Reusable Straw Kit! Compact, collapsible, and it comes with a carabiner clip so you can take it anywhere.Our kit includes a food-grade stainless steel straw with a soft silicone tip so your lips and teeth are protected, as well as a free cleaning brush for effortless cleaning—meaning every time you drink, it’ll taste exactly how you want it.This Reusable Straw Kit makes every sip convenient and hassle-free wherever you are.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/351.png?v=1734684906&width=1080",
      "url": "https://shop.zuscoffee.com/products/zus-reusable-straw-kit-1s?_pos=7&_fid=a8ffe8a86&_ss=c"
    }
  ],
  "count": 5,
  "top_k": 5
}
```


**Status:** Success - Found 5 product(s)


---



### Example 3: Search for Reusable Straws

**Request:**

```
GET /products?query=reusable straw&top_k=3
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "reusable straw",
  "products": [
    {
      "name": "Reusable Straw Kit",
      "category": "Drinkware Accessories",
      "price": "RM16.90",
      "description": "Sustainable, convenient sips.Say goodbye to single-use straws with our Reusable Straw Kit! Compact, collapsible, and it comes with a carabiner clip so you can take it anywhere.Our kit includes a food-grade stainless steel straw with a soft silicone tip so your lips and teeth are protected, as well as a free cleaning brush for effortless cleaning—meaning every time you drink, it’ll taste exactly how you want it.This Reusable Straw Kit makes every sip convenient and hassle-free wherever you are.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/351.png?v=1734684906&width=1080",
      "url": "https://shop.zuscoffee.com/products/zus-reusable-straw-kit-1s?_pos=7&_fid=a8ffe8a86&_ss=c"
    },
    {
      "name": "[Corak Malaysia] Reusable Straw Kit",
      "category": "Drinkware Accessories",
      "price": "RM16.90",
      "description": "Bye-bye single-use straws and hello to sustainable style with the ZUS Reusable Straw Kit! Compact, collapsible, and designed with a carabiner clip, it’s easy to carry wherever you go. Made from food-grade stainless steel with a soft silicone tip to protect your lips and teeth, it’s safe, durable, and simple to clean with the included brush.Whether at home or on the move, the ZUS Reusable Straw Kit keeps every sip convenient and hassle-free.Celebrate local heritage with three stunning new Corak Malaysia designs—available now.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/62_b565f01c-8f6a-487c-bb5f-241958f9b7ff.png?v=1746778301&width=1080",
      "url": "https://shop.zuscoffee.com/products/zus-corak-malaysia-reusable-straw-kit?_pos=4&_fid=a8ffe8a86&_ss=c"
    },
    {
      "name": "ZUS® Buddy Reusable Straw Set",
      "category": "Drinkware Accessories",
      "price": "RM39.00",
      "description": "An adorable companion on straws or pens!A fun and functional collectible set to add a cutesy flair to your everyday drinks!Our ZUS Buddy Silicone Straw Caps fit perfectly onto any straw so it stays sparkling clean between sips. They’re easily adjustable, durable, and adorably designed!Each set includes 6 ZUS Buddy Silicone Straw Caps, 6 Reusable Straws, and 6 Cleaning Brushes.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/FINAL_DONE_Shopify-ProductListingCover_34.png?v=1743070525&width=1080",
      "url": "https://shop.zuscoffee.com/products/zus-buddy-reusable-straw-set?_pos=5&_fid=a8ffe8a86&_ss=c"
    }
  ],
  "count": 3,
  "top_k": 3
}
```


**Status:** Success - Found 3 product(s)


---



### Example 4: Search for Bottles

**Request:**

```
GET /products?query=bottle&top_k=2
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "bottle",
  "products": [
    {
      "name": "All Day Cup Aqua | 500ml",
      "category": "Tumbler",
      "price": "RM79.00",
      "description": "Your drinks All Day, everyday.When you’re the life of the party, you’ll find yourself gravitating towards experiences that can be shared with others. You’re like the endless water: expansive, an adventure waiting to unfold. You’re never in one place when there’s a whole world out there.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/DesignYourOwn-badge.svg?v=1753188579",
      "url": "https://shop.zuscoffee.com/products/all-day-cup-500ml-17oz-aqua-collection?_pos=3&_fid=a8ffe8a86&_ss=c"
    },
    {
      "name": "Reusable Straw Kit",
      "category": "Drinkware Accessories",
      "price": "RM16.90",
      "description": "Sustainable, convenient sips.Say goodbye to single-use straws with our Reusable Straw Kit! Compact, collapsible, and it comes with a carabiner clip so you can take it anywhere.Our kit includes a food-grade stainless steel straw with a soft silicone tip so your lips and teeth are protected, as well as a free cleaning brush for effortless cleaning—meaning every time you drink, it’ll taste exactly how you want it.This Reusable Straw Kit makes every sip convenient and hassle-free wherever you are.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/351.png?v=1734684906&width=1080",
      "url": "https://shop.zuscoffee.com/products/zus-reusable-straw-kit-1s?_pos=7&_fid=a8ffe8a86&_ss=c"
    }
  ],
  "count": 2,
  "top_k": 2
}
```


**Status:** Success - Found 2 product(s)


---



### Failure Cases


### Example 1: No Results Found (Product Not in Drinkware)

**Request:**

```
GET /products?query=coffee beans&top_k=3
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "coffee beans",
  "products": [
    {
      "name": "Stainless Steel Mug | 420ml",
      "category": "Mugs",
      "price": "RM59.00",
      "description": "Coffee smells better outdoors.Does it? I guess it's time to find out! Made for those who cherish the outdoors or simply just prefer sipping their coffee through a mug. Made from durable 304 stainless steel, features double-wall vacuum insulation to keep your drinks hot or cold up to 5 hours.No matter where your journey takes you—whether it’s a roadside coffee break to \"heal\" or a moment in the mountains surrounded by good company—we’re more than just a mug for great coffee. We’re the small comfort you can always count on, wherever the road may lead.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/396.png?v=1738069660&width=1080",
      "url": "https://shop.zuscoffee.com/products/zus-stainless-steel-mug-420ml?_pos=6&_fid=a8ffe8a86&_ss=c"
    },
    {
      "name": "All Day Cup Mountain | 500ml",
      "category": "Tumbler",
      "price": "RM79.00",
      "description": "Your drinks All Day, everyday.Maybe quietude and constancy are your mottos, or you feel at home amongst the fresh, clean air of higher altitudes. As steadfast as the tall trees, you’ve got a grounded confidence about you that speaks of surety, of someone who knows what they want and moves to achieve it.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/DesignYourOwn-badge.svg?v=1753188579",
      "url": "https://shop.zuscoffee.com/products/all-day-cup-500ml-17oz-mountain-collection?_pos=2&_fid=a8ffe8a86&_ss=c"
    },
    {
      "name": "All Day Cup Aqua | 500ml",
      "category": "Tumbler",
      "price": "RM79.00",
      "description": "Your drinks All Day, everyday.When you’re the life of the party, you’ll find yourself gravitating towards experiences that can be shared with others. You’re like the endless water: expansive, an adventure waiting to unfold. You’re never in one place when there’s a whole world out there.",
      "image_url": "https://shop.zuscoffee.com/cdn/shop/files/DesignYourOwn-badge.svg?v=1753188579",
      "url": "https://shop.zuscoffee.com/products/all-day-cup-500ml-17oz-aqua-collection?_pos=3&_fid=a8ffe8a86&_ss=c"
    }
  ],
  "count": 3,
  "top_k": 3
}
```


**Status:** Success - Found 3 product(s)


---



### Example 2: Invalid top_k Parameter

**Request:**

```
GET /products?query=mug&top_k=100
```


**Response Status:** 422


**Response Body:**

```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": [
        "query",
        "top_k"
      ],
      "msg": "Input should be less than or equal to 10",
      "input": "100",
      "ctx": {
        "le": 10
      }
    }
  ]
}
```


**Status:** Failed - HTTP 422


---



## Calculator Endpoint (`/calculator`)


### Success Cases


### Example 1: Calculate 15% of 100

**Request:**

```
POST /calculator/
```


**Request Body:**

```json
{
  "expression": "100 * 0.15"
}
```


**Response Status:** 200


**Response Body:**

```json
{
  "success": true,
  "result": 15.0,
  "message": "Calculation result: 15.0"
}
```


**Status:** Success - Result: 15.0


---



### Example 2: Simple Addition

**Request:**

```
POST /calculator/
```


**Request Body:**

```json
{
  "expression": "250 + 50"
}
```


**Response Status:** 200


**Response Body:**

```json
{
  "success": true,
  "result": 300,
  "message": "Calculation result: 300"
}
```


**Status:** Success - Result: 300


---



### Example 3: Complex Expression

**Request:**

```
POST /calculator/
```


**Request Body:**

```json
{
  "expression": "(100 + 50) * 2"
}
```


**Response Status:** 200


**Response Body:**

```json
{
  "success": true,
  "result": 300,
  "message": "Calculation result: 300"
}
```


**Status:** Success - Result: 300


---



### Example 4: Division

**Request:**

```
POST /calculator/
```


**Request Body:**

```json
{
  "expression": "1000 / 4"
}
```


**Response Status:** 200


**Response Body:**

```json
{
  "success": true,
  "result": 250.0,
  "message": "Calculation result: 250.0"
}
```


**Status:** Success - Result: 250.0


---



### Failure Cases


### Example 1: Invalid Expression

**Request:**

```
POST /calculator/
```


**Request Body:**

```json
{
  "expression": "invalid expression"
}
```


**Response Status:** 200


**Response Body:**

```json
{
  "success": false,
  "result": null,
  "message": "I was unable to help with that request right now. Would you like to explore our products or outlets instead?"
}
```


**Status:** Failed - I was unable to help with that request right now. Would you like to explore our products or outlets instead?


---



### Example 2: Division by Zero

**Request:**

```
POST /calculator/
```


**Request Body:**

```json
{
  "expression": "10 / 0"
}
```


**Response Status:** 200


**Response Body:**

```json
{
  "success": false,
  "result": null,
  "message": "I was unable to help with that request right now. Would you like to explore our products or outlets instead?"
}
```


**Status:** Failed - I was unable to help with that request right now. Would you like to explore our products or outlets instead?


---



## Outlets Endpoint (`/outlets`)


### Success Cases


### Example 1: Find Outlets by Location

**Request:**

```
GET /outlets?query=outlets in Kuala Lumpur
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "outlets in Kuala Lumpur",
  "sql": "SELECT * FROM outlets WHERE LOWER(name) LIKE '%kuala lumpur%' OR LOWER(address) LIKE '%kuala lumpur%' OR LOWER(city) LIKE '%kuala lumpur%' OR LOWER(state) LIKE '%kuala lumpur%' LIMIT 3;",
  "success": true,
  "results": [
    {
      "id": 3,
      "name": "ZUS Coffee - Bandar Menjalara",
      "address": "37, Jalan 3/62a, Bandar Menjalara, 52200 Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur, Malaysia",
      "city": "Kuala Lumpur",
      "state": "Kuala Lumpur",
      "postcode": "52200",
      "latitude": 3.1950509,
      "longitude": 101.6298663,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 8:00 AM – 9:40 PM; Tuesday: 8:00 AM – 9:40 PM; Wednesday: 8:00 AM – 9:40 PM; Thursday: 8:00 AM – 9:40 PM; Friday: 8:00 AM – 9:40 PM; Saturday: 8:00 AM – 9:40 PM; Sunday: 8:00 AM – 9:40 PM",
      "open_time": "08:00:00",
      "close_time": "21:40:00",
      "business_status": "OPERATIONAL"
    },
    {
      "id": 5,
      "name": "ZUS Coffee - LSH33 Sentul",
      "address": "Laman Seri Harmoni (LSH33, 3, Jln Batu Muda Tambahan 3, Sentul, 51100 Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur, Malaysia",
      "city": "Kuala Lumpur",
      "state": "Kuala Lumpur",
      "postcode": "51100",
      "latitude": 3.2090371,
      "longitude": 101.6922523,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 7:00 AM – 10:40 PM; Tuesday: 7:00 AM – 10:40 PM; Wednesday: 7:00 AM – 10:40 PM; Thursday: 7:00 AM – 10:40 PM; Friday: 7:00 AM – 10:40 PM; Saturday: 7:00 AM – 10:40 PM; Sunday: 7:00 AM – 10:40 PM",
      "open_time": "07:00:00",
      "close_time": "22:40:00",
      "business_status": "OPERATIONAL"
    },
    {
      "id": 7,
      "name": "ZUS Coffee - AEON BiG Wangsa Maju",
      "address": "6, Section 5, AEON BIG, F1 - 11, Jalan 8/27a, Wangsa Maju, 53300 Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur, Malaysia",
      "city": "Kuala Lumpur",
      "state": "Kuala Lumpur",
      "postcode": "53300",
      "latitude": 3.1965542,
      "longitude": 101.7433836,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 10:00 AM – 9:40 PM; Tuesday: 10:00 AM – 9:40 PM; Wednesday: 10:00 AM – 9:40 PM; Thursday: 10:00 AM – 9:40 PM; Friday: 10:00 AM – 9:40 PM; Saturday: 10:00 AM – 9:40 PM; Sunday: 10:00 AM – 9:40 PM",
      "open_time": "10:00:00",
      "close_time": "21:40:00",
      "business_status": "OPERATIONAL"
    }
  ],
  "count": 3,
  "error": null
}
```


**Status:** Success - Found 3 outlet(s)


---



### Example 2: Find Outlets with Drive-Thru

**Request:**

```
GET /outlets?query=which outlets have drive thru
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "which outlets have drive thru",
  "sql": "SELECT * FROM outlets WHERE LOWER(name) LIKE '%drive thru%' OR LOWER(address) LIKE '%drive thru%' OR LOWER(city) LIKE '%drive thru%' OR LOWER(state) LIKE '%drive thru%' LIMIT 3;",
  "success": true,
  "results": [],
  "count": 0,
  "error": null
}
```


**Status:** Success - Found 0 outlet(s)


---



### Example 3: Find Outlets with WiFi in Specific Area

**Request:**

```
GET /outlets?query=outlets with wifi in Petaling Jaya
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "outlets with wifi in Petaling Jaya",
  "sql": "SELECT * FROM outlets WHERE LOWER(name) LIKE '%wifi%' OR LOWER(address) LIKE '%wifi%' OR LOWER(city) LIKE '%petaling jaya%' OR LOWER(state) LIKE '%petaling jaya%' LIMIT 3;",
  "success": true,
  "results": [
    {
      "id": 9,
      "name": "ZUS Coffee - Damansara Perdana, Petaling Jaya",
      "address": "12-1 (Ground floor, Jalan PJU 8/5e, Bandar Damansara Perdana, 47820 Petaling Jaya, Selangor, Malaysia",
      "city": "Petaling Jaya",
      "state": "Selangor",
      "postcode": "47820",
      "latitude": 3.1659786,
      "longitude": 101.6061283,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 7:00 AM – 10:40 PM; Tuesday: 7:00 AM – 10:40 PM; Wednesday: 7:00 AM – 10:40 PM; Thursday: 7:00 AM – 10:40 PM; Friday: 7:00 AM – 10:40 PM; Saturday: 7:00 AM – 10:40 PM; Sunday: 7:00 AM – 10:40 PM",
      "open_time": "07:00:00",
      "close_time": "22:40:00",
      "business_status": "OPERATIONAL"
    },
    {
      "id": 27,
      "name": "ZUS Coffee - Uptown Damansara, Petaling Jaya",
      "address": "44-G (Ground Floor, Jalan SS21/39, Damansara Utama, 47400 Petaling Jaya, Selangor, Malaysia",
      "city": "Petaling Jaya",
      "state": "Selangor",
      "postcode": "47400",
      "latitude": 3.135596,
      "longitude": 101.6214604,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 7:00 AM – 10:40 PM; Tuesday: 7:00 AM – 10:40 PM; Wednesday: 7:00 AM – 10:40 PM; Thursday: 7:00 AM – 10:40 PM; Friday: 7:00 AM – 10:40 PM; Saturday: 7:00 AM – 10:40 PM; Sunday: 7:00 AM – 10:40 PM",
      "open_time": "07:00:00",
      "close_time": "22:40:00",
      "business_status": "OPERATIONAL"
    },
    {
      "id": 34,
      "name": "ZUS Coffee - Dataran Glomac, Kelana Jaya",
      "address": "C-G-05 (Ground Floor, Jalan SS 6/5b, Dataran Glomac, 47301 Petaling Jaya, Selangor, Malaysia",
      "city": "Petaling Jaya",
      "state": "Selangor",
      "postcode": "47301",
      "latitude": 3.102733,
      "longitude": 101.6001862,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 7:00 AM – 10:40 PM; Tuesday: 7:00 AM – 10:40 PM; Wednesday: 7:00 AM – 10:40 PM; Thursday: 7:00 AM – 10:40 PM; Friday: 7:00 AM – 10:40 PM; Saturday: 7:00 AM – 10:40 PM; Sunday: 7:00 AM – 10:40 PM",
      "open_time": "07:00:00",
      "close_time": "22:40:00",
      "business_status": "OPERATIONAL"
    }
  ],
  "count": 3,
  "error": null
}
```


**Status:** Success - Found 3 outlet(s)


---



### Example 4: Check Operating Hours

**Request:**

```
GET /outlets?query=what time does ZUS Coffee KLCC open
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "what time does ZUS Coffee KLCC open",
  "sql": "SELECT open_time FROM outlets WHERE LOWER(name) LIKE '%zus coffee%' AND LOWER(name) LIKE '%klcc%'",
  "success": true,
  "results": [
    {
      "open_time": "07:00:00"
    }
  ],
  "count": 1,
  "error": null
}
```


**Status:** Success - Found 1 outlet(s)


---



### Example 5: List All Outlets

**Request:**

```
GET /outlets?query=show me all outlets
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "show me all outlets",
  "sql": "SELECT * FROM outlets LIMIT 3;",
  "success": true,
  "results": [
    {
      "id": 1,
      "name": "ZUS Coffee - Temu Business Centre City Of Elmina",
      "address": "No 5 (Ground Floor), Jalan Eserina AA U16/AA Elmina, East, Seksyen U16, 40150 Shah Alam, Selangor, Malaysia",
      "city": "Shah Alam",
      "state": "Selangor",
      "postcode": "40150",
      "latitude": 3.1858012,
      "longitude": 101.5265532,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 8:00 AM – 9:40 PM; Tuesday: 8:00 AM – 9:40 PM; Wednesday: 8:00 AM – 9:40 PM; Thursday: 8:00 AM – 9:40 PM; Friday: 8:00 AM – 9:40 PM; Saturday: 8:00 AM – 9:40 PM; Sunday: 8:00 AM – 9:40 PM",
      "open_time": "08:00:00",
      "close_time": "21:40:00",
      "business_status": "OPERATIONAL"
    },
    {
      "id": 2,
      "name": "ZUS Coffee - Spectrum Shopping Mall",
      "address": "Lot CW-5 Cafe Walk, Ground Floor Spectrum Shopping Mall Jalan Wawasan Ampang, 4, 2, Bandar Baru Ampang, 68000 Ampang, Selangor, Malaysia",
      "city": "Ampang",
      "state": "Selangor",
      "postcode": "68000",
      "latitude": 3.1456372,
      "longitude": 101.7645605,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 8:00 AM – 9:40 PM; Tuesday: 8:00 AM – 9:40 PM; Wednesday: 8:00 AM – 9:40 PM; Thursday: 8:00 AM – 9:40 PM; Friday: 8:00 AM – 9:40 PM; Saturday: 8:00 AM – 9:40 PM; Sunday: 8:00 AM – 9:40 PM",
      "open_time": "08:00:00",
      "close_time": "21:40:00",
      "business_status": "OPERATIONAL"
    },
    {
      "id": 3,
      "name": "ZUS Coffee - Bandar Menjalara",
      "address": "37, Jalan 3/62a, Bandar Menjalara, 52200 Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur, Malaysia",
      "city": "Kuala Lumpur",
      "state": "Kuala Lumpur",
      "postcode": "52200",
      "latitude": 3.1950509,
      "longitude": 101.6298663,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 8:00 AM – 9:40 PM; Tuesday: 8:00 AM – 9:40 PM; Wednesday: 8:00 AM – 9:40 PM; Thursday: 8:00 AM – 9:40 PM; Friday: 8:00 AM – 9:40 PM; Saturday: 8:00 AM – 9:40 PM; Sunday: 8:00 AM – 9:40 PM",
      "open_time": "08:00:00",
      "close_time": "21:40:00",
      "business_status": "OPERATIONAL"
    }
  ],
  "count": 3,
  "error": null
}
```


**Status:** Success - Found 3 outlet(s)


---



### Failure Cases


### Example 1: Dangerous SQL Attempt (Should be Blocked)

**Request:**

```
GET /outlets?query=delete all outlets
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "delete all outlets",
  "sql": "-- BLOCKED: Dangerous operation detected: delete all outlets",
  "success": false,
  "results": [],
  "count": 0,
  "error": "Invalid query: Only SELECT queries are allowed"
}
```


**Status:** Failed - Invalid query: Only SELECT queries are allowed


---



### Example 2: Nonsense Query (Should Return No Results)

**Request:**

```
GET /outlets?query=asdfghjkl random nonsense
```


**Response Status:** 200


**Response Body:**

```json
{
  "query": "asdfghjkl random nonsense",
  "sql": "SELECT * FROM outlets WHERE LOWER(name) LIKE '%asdfghjkl%' OR LOWER(address) LIKE '%asdfghjkl%' OR LOWER(city) LIKE '%asdfghjkl%' OR LOWER(state) LIKE '%asdfghjkl%' LIMIT 3;",
  "success": true,
  "results": [],
  "count": 0,
  "error": null
}
```


**Status:** Success - Found 0 outlet(s)


---



## Nearest Outlets Endpoint (`/outlets/nearest`)


### Success Cases


### Example 1: Find 3 Nearest Outlets (Petaling Jaya Area)

**Request:**

```
POST /outlets/nearest
```


**Request Body:**

```json
{
  "latitude": 3.1478,
  "longitude": 101.6953,
  "limit": 3
}
```


**Response Status:** 200


**Response Body:**

```json
{
  "success": true,
  "user_location": {
    "latitude": 3.1478,
    "longitude": 101.6953
  },
  "results": [
    {
      "id": 63,
      "name": "ZUS Coffee - Jakel Mall, Kuala Lumpur",
      "address": "Lot SC.02 & SC.03, Jakel Mall, Lot 159, Jakel Square, Off, Jalan Munshi Abdullah, City Centre, 50100 Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur, Malaysia",
      "city": "Kuala Lumpur",
      "state": "Kuala Lumpur",
      "postcode": "50100",
      "latitude": 3.1538864,
      "longitude": 101.699588,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 8:00 AM – 8:40 PM; Tuesday: 8:00 AM – 8:40 PM; Wednesday: 8:00 AM – 8:40 PM; Thursday: 8:00 AM – 8:40 PM; Friday: 8:00 AM – 8:40 PM; Saturday: 8:00 AM – 8:40 PM; Sunday: 8:00 AM – 8:40 PM",
      "open_time": "08:00:00",
      "close_time": "20:40:00",
      "business_status": "OPERATIONAL",
      "distance_km": 0.83
    },
    {
      "id": 73,
      "name": "ZUS Coffee - Semua House",
      "address": "GF.04, Ground Floor, Semua House, Jalan Bunus 6, City Centre, 50100 Wilayah Persekutuan, Wilayah Persekutuan Kuala Lumpur, Malaysia",
      "city": "Kuala Lumpur",
      "state": "Kuala Lumpur",
      "postcode": "50100",
      "latitude": 3.1550605,
      "longitude": 101.6972503,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 9:00 AM – 7:40 PM; Tuesday: 9:00 AM – 7:40 PM; Wednesday: 9:00 AM – 7:40 PM; Thursday: 9:00 AM – 7:40 PM; Friday: 9:00 AM – 7:40 PM; Saturday: 9:00 AM – 7:40 PM; Sunday: 9:00 AM – 7:40 PM",
      "open_time": "09:00:00",
      "close_time": "19:40:00",
      "business_status": "OPERATIONAL",
      "distance_km": 0.84
    },
    {
      "id": 47,
      "name": "ZUS Coffee - Pertama Complex, Kuala Lumpur",
      "address": "Kiosk No. 3, Kompleks Pertama, Jalan Tuanku Abdul Rahman, Chow Kit, 50100 Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur, Malaysia",
      "city": "Kuala Lumpur",
      "state": "Kuala Lumpur",
      "postcode": "50100",
      "latitude": 3.1574179,
      "longitude": 101.6955075,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 7:00 AM – 9:40 PM; Tuesday: 7:00 AM – 9:40 PM; Wednesday: 7:00 AM – 9:40 PM; Thursday: 7:00 AM – 9:40 PM; Friday: 7:00 AM – 9:40 PM; Saturday: 7:00 AM – 9:40 PM; Sunday: 7:00 AM – 9:40 PM",
      "open_time": "07:00:00",
      "close_time": "21:40:00",
      "business_status": "OPERATIONAL",
      "distance_km": 1.07
    }
  ],
  "count": 3,
  "error": null
}
```


**Status:** Success - Found 3 nearest outlet(s)


---



### Failure Cases


### Example 1: Invalid Coordinates

**Request:**

```
POST /outlets/nearest
```


**Request Body:**

```json
{
  "latitude": 999,
  "longitude": 999,
  "limit": 3
}
```


**Response Status:** 200


**Response Body:**

```json
{
  "success": true,
  "user_location": {
    "latitude": 999.0,
    "longitude": 999.0
  },
  "results": [
    {
      "id": 16,
      "name": "ZUS Coffee - MAB Academy Campus Sepang",
      "address": "Level 1, MAB Academy (MABA Campus) Building, Southern Support Zone, Kuala Lumpur International Airport, 64000 Sepang, Selangor, Malaysia",
      "city": "Sepang",
      "state": "Selangor",
      "postcode": "64000",
      "latitude": 2.7281907,
      "longitude": 101.7179475,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 9:00 AM – 5:10 PM; Tuesday: 9:00 AM – 5:10 PM; Wednesday: 9:00 AM – 5:10 PM; Thursday: 9:00 AM – 5:10 PM; Friday: 9:00 AM – 5:10 PM; Saturday: Closed; Sunday: Closed",
      "open_time": "09:00:00",
      "close_time": "17:10:00",
      "business_status": "OPERATIONAL",
      "distance_km": 11310.51
    },
    {
      "id": 113,
      "name": "ZUS Coffee - Gateway@KLIA Terminal 2 (Departure Hall, Level 3)",
      "address": "Malaysia, Selangor, Sepang, Kuala Lumpur International Airport, Gateway@KLIA2邮政编码: 43900",
      "city": "Kuala Lumpur",
      "state": "Selangor",
      "postcode": "43900",
      "latitude": 2.74293,
      "longitude": 101.6863441,
      "phone": null,
      "phone_international": null,
      "operating_hours": "Monday: 7:00 AM – 10:40 PM; Tuesday: 7:00 AM – 10:40 PM; Wednesday: 7:00 AM – 10:40 PM; Thursday: 7:00 AM – 10:40 PM; Friday: 7:00 AM – 10:40 PM; Saturday: 7:00 AM – 10:40 PM; Sunday: 7:00 AM – 10:40 PM",
      "open_time": "07:00:00",
      "close_time": "22:40:00",
      "business_status": "OPERATIONAL",
      "distance_km": 11312.18
    },
    {
      "id": 114,
      "name": "ZUS Coffee - Gateway@KLIA Terminal 2 (Arrival Hall, Level 2)",
      "address": "Lot No. L2-90B, Level 2 gateway@KLIA2, Lbh KLIA, Kuala Lumpur International Airport, 43900 Selangor, Malaysia",
      "city": "Kuala Lumpur",
      "state": "Selangor",
      "postcode": "43900",
      "latitude": 2.7446513,
      "longitude": 101.6852555,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 7:00 AM – 10:40 PM; Tuesday: 7:00 AM – 10:40 PM; Wednesday: 7:00 AM – 10:40 PM; Thursday: 7:00 AM – 10:40 PM; Friday: 7:00 AM – 10:40 PM; Saturday: 7:00 AM – 10:40 PM; Sunday: 7:00 AM – 10:40 PM",
      "open_time": "07:00:00",
      "close_time": "22:40:00",
      "business_status": "OPERATIONAL",
      "distance_km": 11312.37
    }
  ],
  "count": 3,
  "error": null
}
```


**Status:** Success - Found 3 nearest outlet(s)


---



### Example 2: Missing Limit Parameter

**Request:**

```
POST /outlets/nearest
```


**Request Body:**

```json
{
  "latitude": 3.1478,
  "longitude": 101.6953
}
```


**Response Status:** 200


**Response Body:**

```json
{
  "success": true,
  "user_location": {
    "latitude": 3.1478,
    "longitude": 101.6953
  },
  "results": [
    {
      "id": 63,
      "name": "ZUS Coffee - Jakel Mall, Kuala Lumpur",
      "address": "Lot SC.02 & SC.03, Jakel Mall, Lot 159, Jakel Square, Off, Jalan Munshi Abdullah, City Centre, 50100 Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur, Malaysia",
      "city": "Kuala Lumpur",
      "state": "Kuala Lumpur",
      "postcode": "50100",
      "latitude": 3.1538864,
      "longitude": 101.699588,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 8:00 AM – 8:40 PM; Tuesday: 8:00 AM – 8:40 PM; Wednesday: 8:00 AM – 8:40 PM; Thursday: 8:00 AM – 8:40 PM; Friday: 8:00 AM – 8:40 PM; Saturday: 8:00 AM – 8:40 PM; Sunday: 8:00 AM – 8:40 PM",
      "open_time": "08:00:00",
      "close_time": "20:40:00",
      "business_status": "OPERATIONAL",
      "distance_km": 0.83
    },
    {
      "id": 73,
      "name": "ZUS Coffee - Semua House",
      "address": "GF.04, Ground Floor, Semua House, Jalan Bunus 6, City Centre, 50100 Wilayah Persekutuan, Wilayah Persekutuan Kuala Lumpur, Malaysia",
      "city": "Kuala Lumpur",
      "state": "Kuala Lumpur",
      "postcode": "50100",
      "latitude": 3.1550605,
      "longitude": 101.6972503,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 9:00 AM – 7:40 PM; Tuesday: 9:00 AM – 7:40 PM; Wednesday: 9:00 AM – 7:40 PM; Thursday: 9:00 AM – 7:40 PM; Friday: 9:00 AM – 7:40 PM; Saturday: 9:00 AM – 7:40 PM; Sunday: 9:00 AM – 7:40 PM",
      "open_time": "09:00:00",
      "close_time": "19:40:00",
      "business_status": "OPERATIONAL",
      "distance_km": 0.84
    },
    {
      "id": 47,
      "name": "ZUS Coffee - Pertama Complex, Kuala Lumpur",
      "address": "Kiosk No. 3, Kompleks Pertama, Jalan Tuanku Abdul Rahman, Chow Kit, 50100 Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur, Malaysia",
      "city": "Kuala Lumpur",
      "state": "Kuala Lumpur",
      "postcode": "50100",
      "latitude": 3.1574179,
      "longitude": 101.6955075,
      "phone": "012-816 1340",
      "phone_international": "+60 12-816 1340",
      "operating_hours": "Monday: 7:00 AM – 9:40 PM; Tuesday: 7:00 AM – 9:40 PM; Wednesday: 7:00 AM – 9:40 PM; Thursday: 7:00 AM – 9:40 PM; Friday: 7:00 AM – 9:40 PM; Saturday: 7:00 AM – 9:40 PM; Sunday: 7:00 AM – 9:40 PM",
      "open_time": "07:00:00",
      "close_time": "21:40:00",
      "business_status": "OPERATIONAL",
      "distance_km": 1.07
    }
  ],
  "count": 3,
  "error": null
}
```


**Status:** Success - Found 3 nearest outlet(s)


---



## Health Checks


### Products Health Check

**Request:**

```
GET /products/health?
```


**Response Status:** 200


**Response Body:**

```json
{
  "status": "healthy",
  "products_loaded": 11
}
```


**Status:** Success


---



### Calculator Health Check

**Request:**

```
GET /calculator/health?
```


**Response Status:** 200


**Response Body:**

```json
{
  "status": "healthy"
}
```


**Status:** Success


---



### Outlets Health Check

**Request:**

```
GET /outlets/health?
```


**Response Status:** 200


**Response Body:**

```json
{
  "status": "healthy",
  "outlets_count": 142
}
```


**Status:** Success


---



## Summary

All transcripts captured from live API responses.

Server: https://zus-coffee-chatbot-api-702670372085.asia-southeast1.run.app

Timestamp: 2025-10-23 19:26:14
