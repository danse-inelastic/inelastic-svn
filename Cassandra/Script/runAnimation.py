   
for i in range(int(nbStep)):
    level = (level_start + (i*step))
    isoLevel.updateIsoLevel(plasma_dataset, level , 1, 0,level_start, 0.0) 
    pipeLineManager.getCassandraView().rotate(.2/scaleFactor,0.0)
    pipeLineManager.validateViewAndWait()

    filePath = outputImageBasePath
    if(i>99):
        filePath += `i`
    elif(i>9):  
        filePath += "0" + `i`
    else:
        filePath += "00" + `i`
        
    #view.HardCopy(filePath+".tiff", 1);
