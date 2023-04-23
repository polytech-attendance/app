import express from "express"
import bodyParser from 'body-parser'
import cheerio from "cheerio";
import jsdom from 'jsdom'
import axios from 'axios';
import jQuery from "jquery";
import fs from 'fs'
let classId = 35427;
const app = express();
const PORT = 5173;

app.use(bodyParser.json());
let data1 = [{
    student_id: 1234,
    student_status: 1,
    date : '',
    time: '',
    class_id: 2345,
    group_id: 32}];

//GET handler
// app.get('/',(req,res)=>{
//     fs.readFile('src/lib/schedule.json', 'utf-8', function(err, data) {
//         if (err) {
//         console.error(err);
//         } else {
//             res.send(data);
//         }
//     });

// })
app.get('/api/data', (req, res)=>{
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.send(data);
})

//POST handler
app.post('/api/data', (req,res)=>{
    data.push(req.body);
    res.send('Data added successfully');
})

//Start server
app.listen(PORT, ()=>{
    console.log('Server listening on port ' + PORT);
});