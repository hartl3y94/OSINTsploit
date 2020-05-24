mainjson = {
    "nodes": [
        
    ],

    "links": [
      
    ]
}

data = {
        "id": "2",
        "module": "Facebook",
        "description": "",
        "group": 1 
}

link = {
        "source": "2",
        "target": "1"
    }


mainjson['nodes'].append(data)
mainjson['links'].append(link)

print(mainjson)

