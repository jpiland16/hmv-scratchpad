const express = require('express')
const app = express()
const port = 3000
var path = require('path');

app.use('/public', express.static(__dirname + '/public'));
app.use('/data', express.static(__dirname + '/data'))

app.get('/', (req, res) => {
	res.sendFile(path.join(__dirname+'/views/mainscene.html'))
})

app.listen(port, () => {
	console.log(`Example app listening at http://localhost:${port}`)
})