# AID-PRIGSHARE
## Automation of Indicator Development for Green Space Health Research in QGIS
## Accompanying Script to the PRIGSHARE Reporting Guidelines.

The PRIGSHARE_QGIS_Script will produce green space and greenness indicators in distances from 100-1.500m every 100m automatically. 

A frequent demand in the interdisciplinary field of green space health research is to reduce the effort to assess green space, especially for non-spatial disciplines. Realizing this issue, we developed AID-PRIGSHARE. AID-PRIGSHARE is an open-source script with an easy-to-use user interface that substantially reduces the time-intensive and complex task of green space indicator generation by automatization. AID-PRIGSHARE will simultaneously calculate indicators such as mean greenness, total public green space, access to green infrastructure, and green space uses for distances of 100-1500m in 100m steps around a (home) address if the input layers are provided. This substantially reduces the effort for sensitivity analysis and may support research that aims to understand better the individual characteristics of green spaces and their effect range.

The script requires the input of addresses of individuals (point layer). Other inputs are only necessary for specific calculations (see input parameters below).





---
## BEFORE YOU BEGIN 
Thank you for using the PRIGSHARE algorithm to generate green space indicators.
The validity of the algorithm output will depend on the validity of the input layers provived. Please check the PRIGSHARE Reporting Guidelines (https://doi.org/10.1016/j.envres.2023.115893) for common sources of bias in green space assessment and use the guidelines to eliminate noise from your data as much as possible. 

      Cardinali, M., Beenackers, M. A., van Timmeren, A., & Pottgiesser, U. (2023a). 
      Preferred reporting items in green space health research. 
      Guiding principles for an interdisciplinary field. Environmental Research, 228, 115893. 
      https://doi.org/10.1016/j.envres.2023.115893
    

If you used AID-PRIGSHARE (https://doi.org/10.1016/j.simpa.2023.100506) in your research, please cite the following paper:

      Cardinali, M., Beenackers, M. A., van Timmeren, A., & Pottgiesser, U. (2023b). 
      AID-PRIGSHARE: Automatization of indicator development in green space health research in QGIS. 
      Accompanying script to the PRIGSHARE reporting guidelines. Software Impacts, 100506. 
      https://doi.org/10.1016/j.simpa.2023.100506
     

---

![Fig3 task chains](https://user-images.githubusercontent.com/80674342/222116342-e74ccbd8-9caa-42ed-8c92-0bcf8599c832.png) Task chains of the script




## INSTALLATION
Just open the downloaded file „PRIGSHARE_QGIS_Script.model3“ within the QGIS browser panel with a double-click. This should open an input mask with the following parameters:

## INPUT PARAMETERS 
Please make sure you check all the boxes for those indicators that you want the algorithm to calculate. Otherwise, your input will be ignored.

### Individuals Geolocation
> Mandatory

Please provide a layer with the geolocation of the individuals of your study as a point layer. This will also be the layer, where all calculated spatial indicators will be added to the attribute table. 

Hint: Take care of potential bias. Often geolocation algorithms are not able to find all the addresses and place them in the city center instead. Harder to find are those addresses that are incorrectly identified. Both should be manually corrected BEFORE you use the algorithm. 

### ID_Field (identifier to separate individuals in individual geolocation files)
> Mandatory

Please provide the exact name of the field in your individual geolocation point layer that is a unique identifier for each individual.

### Walkability Layer (Street Network)
>  Needed for to calculate Buffered Service Areas - otherwise optional.

Please provide a line layer with the street network.

### Vegetation Index (needs to be vectorized)
> Needed for Vegetation Assessment - otherwise optional

Please provide a vectorized vegetation index polygon layer. 


### Public Green Space Layer
> Needed for Spatial Assessment - otherwise optional

Please provide a polygon layer with the public green spaces of your study area. 


### Semi-Public Green Spaces (will add SPGS indicator)
> Needed to calculate semi-public green spaces - otherwise optional.

Please provide a polygon layer with the lots of multi-story residential buildings derived from a cadastre map of your study area. 
If provided, the PRIGSHARE algorithm will add the indicator SPGS (Semi-Public Green Space) to the database for people living in these buildings.

### Private Green Space (will add PRGS indicator)
> Needed to calculate private green spaces - otherwise optional.

Please provide a polygon layer with the lots of one-family homes derived from a cadastre map of your study area. 
If provided, the PRIGSHARE algorithm will add the indicator PRGS (Private Green Space) to the database for people with a private garden.


### Buildings (will subtract building footprint from all green spaces if provided)
> Needed to calculate semi-public and private green spaces - otherwise optional.

Please provide a polygon layer with the building footprints of your study area. This layer is needed to subtract building footprint from the plot.

### Green Space Uses (Playgrounds, Sports, Gardening, Social, Cultural,..)
> Needed to assess the potential uses in green spaces around an individual / otherwise optional

Please provide a point layer with the green space uses of your study area. For example a point for every playground, fireplace, urban gardening, sports field, and maybe even walking entries in bigger parks as a proxy for the walkability they provide. If provided, the PRIGSHARE algorithm will add the indicators GS_uses and GS_diversity to the database for distances from 100m - 1500m. Due to limitations in the algorithm the script will only work for this indicator if all 6 point layers are provided. A work around is to create empty layers, if you don't have/don't want to count 6 different uses.

## ADAPTING AND CHANGING THE SCRIPT ##
In order to change the algorithm (e.g. to generate output with more/other distances), you can open the file from the processing toolbox of QGIS and click on „load existing model“. Or you can right-click on the model file in the browser panel and click „edit model“. Here is the documentation to work with the graphical modeler: https://docs.qgis.org/3.22/en/docs/user_manual/processing/modeler.html

---
# Example
<img width="1632" alt="Example Nantes" src="https://user-images.githubusercontent.com/80674342/222807390-a9c94a84-b2d3-4fe5-9374-bda25b88ca13.png">


# Input Mask
<img width="1633" alt="Input Mask Nantes" src="https://user-images.githubusercontent.com/80674342/222807428-23f5905c-dae4-44b1-93df-8c56e2c4a7c6.png">

# Algoritm Output
<img width="1527" alt="Output Example" src="https://user-images.githubusercontent.com/80674342/222808104-d126a918-12a1-46ec-b330-c9a11599652d.png">


---
# Graphical Model
![Fig1 Graphical Model](https://user-images.githubusercontent.com/80674342/224657200-76a8ea44-70f1-4655-8027-a71d4e70496f.jpg)

---
# FAQ

### How long does the calculation take approximately? The calculation time is very long and not progressing for a long time.

A calculation of all indicators takes about 8 hours on a MacBook pro with M1 processor for around 400 observations. Depending on your own machine and the number of observations this might take considerably longer. Even if the loading bar is not progressing for some time and QGIS seems to be frozen, the machine should be working in the background. We suggest running the algorithm before you leave your desk and just letting it run overnight. 

### My system crashed when I try to run the tool with all layers.

For some users QGIS unexpectedly ends when they run the algorithm with all layers requests. This problem seems to be related to the amount of free RAM available. For older machines or those with 8GB of RAM or lower we recommend to close all other applications and/or take a stepwise approach when running the algorithm.  

### The Log shows “no spatial index exists for join layer, performance will be severely degraded”.

Spatial indices simply speed up processing. The warning communicates that the calculation time will be longer without a spatial index, but this will not affect the result. If you have a very large dataset and want to speed up the process, consider adding a spatial index to your layer(s).

### Log shows feature (number) from Layer (name) has invalid geometry and has been skipped.

This means that the some geometry features in your layer cannot be used to calculate the indicators. This might be ignored, depending on the percentage of flawed geometries. For example, several dozens of those messages in a very large walkability layer with 10,000 of lines, might be ignorable. But five of those messages for a public green space layer consisting of 20 polygons should be taken seriously. There are several possible pairs of invalid geometries and solutions that cannot be covered here. 

### Why do I get the message “fails to join attributes by…” and the process failed. 

This error occurs predominantly when the ID field is not filled properly. Please check for spelling mistakes.

### I want to calcualate only specific distances. Can I do that?

Unfortunately this feature is not implemented at the moment. The way the algorithm is designed makes it necessary that every output layer exists, otherwise the process will fail. 

