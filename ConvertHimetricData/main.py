from xml.dom import minidom
import os

path = ""
def run():
    # Change to your appropriate directory
    #dataDir = "C:\\Users\\Research\\Documents\\sketch\\Data\\E85\\New Labeled Documents\\Labeled Summer 2007"
    dataDir = "C:\\Users\\Research\\Documents\\sketch\\Data\\Gate Study Data\\AllLabeledSketches"
    for fileName in os.listdir(dataDir):
        if os.path.splitext(fileName)[1] == ".xml":
            inName = dataDir + "/" + fileName
            #Change to appropriate directory depending on XML
            #outName = os.getcwd() + "\\pixels\\E85 Data\\" + fileName
            outName = os.getcwd() + "\\pixels\\UCR Gate Study Data\\" + fileName
            convertFile(inName, outName)
    
def convertFile(inName, outName):
    print("trying to parse " + inName)
    dom = minidom.parse(inName)
    sketchTag = dom.getElementsByTagName("sketch")[0]
    if sketchTag.getAttribute("units") == "himetric":
        convertPoints(dom)
        convertShapes(dom)
        sketchTag.setAttribute("units", "pixels")
    print("writing to " + outName)
    fd = open(outName, 'w')
    fd.write(dom.toxml())
    fd.close()
    return 1

def convertHimetricToPixel(himetric):
    x = float(himetric)
    pixel = x / 2540 * (1140 / 12)
    return str(max(1, pixel))

def convertPoints(dom):
    points = dom.getElementsByTagName("point")
    for point in points:
        for attr in ["x", "y"]:
            value = point.getAttribute(attr)
            if value != "":
                point.setAttribute(attr, convertHimetricToPixel(value))
    return

def convertShapes(dom):
    shapes = dom.getElementsByTagName("shape")
    for shape in shapes:
        for attr in ["x", "y", "height", "width", "penHeight", "penWidth"]:
            value = shape.getAttribute(attr)
            if value != "":
                shape.setAttribute(attr, convertHimetricToPixel(value))

        typ = shape.getAttribute("type")
        if typ == "Label":
            shape.setAttribute("type", "IO")
    return

if __name__ == '__main__':
    run()
