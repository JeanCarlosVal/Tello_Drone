if (process.env.NODE_ENV !== 'production') {
    require('dotenv').config();
}
const AWS = require("@aws-sdk/client-dynamodb");
const e = require('express');
const express = require('express')
const router = express.Router()

const client = new AWS.DynamoDB({
    region: 'us-east-1',
    credentials: {
        accessKeyId: process.env.DB_ACCESS_KEY_ID,
        secretAccessKey: process.env.DB_SECRET_ACCESS_KEY_ID
    }
});

const leaderboard_param = require("../dynamodb/leaderboard.json")

var leaderboard
var search_results

async function get_leaderboard() {
    try {
        leaderboard = await client.query(leaderboard_param)
    } catch (error) {
        console.log(error)
    }
}

async function get_search(query){
    try {
        search_results = await client.query(query)
    } catch (error) {
        console.log(error)
    }
}

get_leaderboard()

router.get('/', (req, res) => {
    res.render('index')
})

router.get('/leaderboard', (req, res) => {
    const processed_data = process_table()
    res.render('leaderboard', { table: processed_data })
})

router.get('/flights', (req, res) => {
    res.render('flights',{table: ''})
})

router.post('/flights', async (req, res) => {
    let processed_search
    const query = createQuery(req.body.email, req.body.date)
    get_search(query)
    setTimeout(() => {
        if(search_results.Count != 0){
            processed_search = process_search(search_results.Items)
            res.render('flights', {table: processed_search})
        } else{
            res.render('flights', {table: 'No Results'})
        }
    },200)
})

module.exports = router

function process_table() {
    let html = '<table class="table table-hover"><thead><tr><th scope="col">Position</th><th scope="col">Pilot Name</th><th scope="col">Email Address</th><th scope="col">Department</th><th scope="col">Flight ID</th><th scope="col">Flight Time(s)</th></tr></thead><tbody>'

    const items = leaderboard.Items

    for (let i = 0; i < items.length; i++) {
        const element = items[i];
        const pos = i + 1
        html += '<tr> <th scope="col">' + pos + '</th><td>' + element.pilot_name.S + '</td><td>' + element.Email_Address.S + '</td><td>' + element.Department.S + '</td><td>' + element.Flight_Id.S + '</td><td>' + element.Flight_Time_s.N + '</td></tr>'
    }

    html += '</tbody></table>'

    return html
}

function process_search(items){
    let html = '<table class="table table-hover"><thead><tr><th scope="col">Pilot Name</th><th scope="col">Email Address</th><th scope="col">Department</th><th scope="col">Flight ID</th><th scope="col">Flight Time(s)</th><th scope="col">Flight Status</th></tr></thead><tbody>'

    for (let i = 0; i < items.length; i++) {
        const element = items[i];
        let validation
        if(element.Flight_Validation == 'T'){
            validation = 'Successfull'
        }else{
            validation = 'Failed'
        }
        html += '<tr><th scope="col">' + element.pilot_name.S + '</th><td>' + element.Email_Address.S + '</td><td>' + element.Department.S + '</td><td>' + element.Flight_Id.S + '</td><td>' + element.Flight_Time_s.N + '</td><td>' + validation + '</td></tr>'
    }

    html += '</tbody></table>'

    return html
}

function createQuery(email, date) {
    const query = {
        "TableName": "drone_flights",
        "ExpressionAttributeValues": {
            ":email": { "S": email },
            ":date": {"S": date}
        },
        "KeyConditionExpression": "Email_Address = :email and begins_with (Flight_Id, :date)",
        "ProjectionExpression": "pilot_name, Email_Address, Flight_Id, Department, Flight_Time_s, Flight_Validation"
    }
    return query
}