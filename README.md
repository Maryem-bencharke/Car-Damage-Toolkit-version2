# Car-Damage-Toolkit-version2 
![app_gif](cardamage.gif)

## :scroll: Presentation
These project is another version of my previous project [Car Damage Toolkit](https://github.com/LiganiumInc/Car-Damage-Toolkit) with new awesome features :<br>
* A pretty Interface powered by `vuejs`  and `Bulma CSS` 
---
* Backend handled by `Django Rest Framework` to facilitate API building
---
* `Axios` to facilitate Requests on the API
---
* `Openvino`  Toolkit to transform each Tensorflow model into an Intermediate Represention  to allow a fast Inference on CPU <br><br>
<img src="https://user-images.githubusercontent.com/15709723/127779167-9d33dcc6-9001-4d74-a089-8248310092fe.png"  width="300" height="100">

---

* Possibility to generate a PDF report from Analysis's Result by using `html2pdf.js`

## :hourglass_flowing_sand: Workflow

The Analysis of each image follow these steps : <br>
1. VGG19 model is used to determine if Image is a Car or Not
2. A second model is used to see if there is any damage or Not
3. The aim of the third model is to localize damage following three classes : Front, Rear, Side
4. Finally the last model determine the severity of damages based on three classes : Minor, Moderate, Severe
