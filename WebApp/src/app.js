const path = require('path')
const express = require('express')
const hbs = require('hbs')
const multer = require('multer')
const spawn = require('child_process').spawn
const fs = require('fs')
const { getVideoDurationInSeconds } = require('get-video-duration')

const storage = multer.diskStorage({
    destination : './public/uploads/',
    filename : function(req,file,cb){
        cb(null,file.fieldname + '-' + Date.now() + path.extname(file.originalname))
    }
})

const upload = multer({
    storage : storage
}).single('myFile')

const app = express()

const publicDirectory = path.join(__dirname, '../public')
const viewsPath = path.join(__dirname, '../templates/views')
const partialsPath = path.join(__dirname, '../templates/partials')

app.set('view engine', 'hbs')
app.set('views',viewsPath)
hbs.registerPartials(partialsPath)

app.use(express.static(publicDirectory))
app.use(express.urlencoded({extended: true}))

app.get('', (req,res) => {
    res.render('index',{
        title : 'Deepfake Detection',
        name : 'Nahi Degi Mitra Mandal'
    })

    
})


app.get('/Scan',(req,res) => {
    res.render('Scan',{
        title : 'Deepfake Detection',
        name : 'Nahi Degi Mitra Mandal'
    })
})

app.get('/about', (req,res) => {
    res.render('about_us',{
        title : 'About',
        name : 'Nahi Degi Mitra Mandal'
    })
})

app.post('/upload', (req,res) => {
    upload(req,res,(err) => {
        if(err)
        {
            res.render('index',{
                ERROR : 'Unable to Fetch Data'
            })
        }
        else
        {
            console.log(req.file) 
            const paths = req.file.path
            console.log(paths)
            let v_duration = 0
            var v_size = req.file.size
            v_size = v_size/(1024*1024)
    
            if(req.file != undefined)
            {
                const output = spawn('python3', ['/home/soham/DFD/DFD/classify/driver.py','./' + paths])
                output.stdout.on('data', data => {
                    getVideoDurationInSeconds(paths).then((duration) => {
                        var temp = data.toString('UTF8')
                        var verdict = ''
                        var i=0;
                        for(i = 0;temp[i]!='\n';i++)
                        {
                            verdict += temp[i]
                        }
                        var val = ''
                        i++
                        while(temp[i]!='\n')
                        {
                            val+=temp[i]
                            i++
                        }
                        console.log(val)
                        res.render('upload',{
                            FILENAME : req.file.originalname,
                            ENCODING : req.file.encoding,
                            SIZE : v_size,
                            DURATION : duration,
                            VERDICT : verdict,
                            AUDIO_DURATION : duration,
                            VALUE : val
                        })
                    })
                })
            }
            else
            {
                if(req.body != undefined)
                {
                    console.log(req.body)
                    const a = JSON.parse(JSON.stringify(req.body))
                    console.log(a.myFile)
                    const URL = a.myFile
                    const file = fs.createWriteStream("./public/uploads/myfile-" + Date.now() +".mp4");
                    const request = app.get(URL,(response) => {
                        response.pipe(file)
                        console.log('Download Complete')
                    })
                }
            }
        }
    })      
})

app.get('/contactus', (req,res) => {
    res.render('contact_us', {
        title : 'Contact Us',
        name : 'Nahi Degi Mitra Mandal'
    })
})

app.get('/help/*', (req,res) => {
    res.render('error',{
        title : 'Error',
        name : 'Yash Biyani',
        text : 'Nahi Degi Mitra Mandal'
    })
})

app.get('*', (req,res) => {
    res.render('error',{
        title : 'Error',
        name : 'Nahi Degi Mitra Mandal',
        text : 'Page not found'
    })
})

app.listen(3000, () => {
    console.log('Server is up on port 3000')
})