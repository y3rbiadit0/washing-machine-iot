#!/bin/bash
# Script to Initialize MongoDB Replica Set with a single node
mongo <<EOF
var config = {
    "_id": "dbrs",
    "version": 1,
    "members": [
        {
            "_id": 1,
            "host": "mongodb1:27017",
            "priority": 1
        },
    ]
};
rs.initiate(config, { force: true });
rs.status();
EOF
