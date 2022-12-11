const express = require('express')
const app = express()
const expressLayouts = require('express-ejs-layouts')
const path = require('path')
const { execArgv } = require('process')

const indexRouter = require('./routes/index')

app.set('view engine', 'ejs')
app.set('views', __dirname + '/views')
app.set('layout', 'layouts/layout')
app.use(expressLayouts)
app.use(express.static('public'))
app.use(express.json())
app.use(express.urlencoded({extended: false}))

app.use('/css', express.static(path.join(__dirname, 'node_modules/bootstrap/dist/css')))
app.use('/js', express.static(path.join(__dirname, 'node_modules/bootstrap/dist/js')))
app.use('/js', express.static(path.join(__dirname, 'node_modules/jquery/dist')))
app.use('/js', express.static(path.join(__dirname, 'node_modules/@popperjs/core/dist/umd')))

app.use('/', indexRouter)

app.listen(process.env.PORT || 3000)
console.log("Server listening on http://localhost:3000")

