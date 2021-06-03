const path = require('path')
const express = require('express')
const hbs = require('hbs')
const multer = require('multer')
const spawn = require('child_process').spawn

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

app.get('', (req,res) => {
    res.render('index',{
        title : 'Deepfake Detection',
        name : 'Nahi Degi Mitra Mandal'
    })

    
})

app.get('/about', (req,res) => {
    res.render('about',{
        title : 'About',
        name : 'Nahi Degi Mitra Mandal'
    })
})

app.post('/upload', (req,res) => {
    upload(req,res,(err) => {
        if(err)
        {
            res.render('index',{
                ERROR : 'Lafde Jhale'
            })
        }
        else
        {
            console.log(req.file)
            const output = spawn('python3', ['/home/soham/DFD/DFD/classify/driver.py','/home/soham/DFD/DFD/WebApp/src' + req.file.path])
            output.stdout.on('data', data => {
                res.render('index',{
                    ERROR : data.toString()
                })
            })
            
        }
    });
})

app.get('/help', (req,res) => {
    res.render('help', {
        title : 'Help',
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