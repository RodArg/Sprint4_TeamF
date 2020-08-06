# Sprint4_TeamF
A repository where Team F will be assembling their web application solution for Citibank

## Running the code
# Command line
From the Sprint4_TeamF or Sprint4_TeamF/TextExtraction directories
* `python TextExtraction/console.py <filename.jpg>`

# Application
From the Sprint4_TeamF directory
* `node app.js`
* localhost:3000

## Dependencies
1. OpenCV
    * used by PyTesseract for image transformations
    * `pip install opencv-python` 

2. PyTesseract
    * Linux:
        * `sudo apt-get update`
        * `sudo apt-get install tesseract-ocr`
        * `sudo apt-get install libtesseract-dev`
    * Mac:
        * Follow [this guide](http://macappstore.org/tesseract/)
    * Windows:
        * Follow [this guide](https://towardsdatascience.com/read-text-from-image-with-one-line-of-python-code-c22ede074cac)

3. App.js
   * `npm install express`
   * `npm install handlebars`
      * `or yarn add handlebars`
   * `npm install python-shell`
   * `npm install hbs`

        
## Notes
* GCV currently requires locally stored credentials
