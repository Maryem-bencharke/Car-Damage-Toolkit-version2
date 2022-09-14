<template>
    <div class="page-analysis">
        <div class="columns is-multiline">

            <div id="element-to-convert" class="columns">

                <div class="column">
                    <div>
                        <figure >
                            <img v-bind:src="Car.get_image" alt="" >
                        </figure>
                   </div>
                </div>

                <div class="ml-6 mt-4" v-if=" ! result">
                        <a class="button is-danger " @click="startanalysis" >Launch Analysis</a>
                        <p  v-if="loading" style="color:red; margin-top: 20px;"> Analysis in progress .....<br> Please wait </p>
                </div>
                <!-- v-if="loading" -->


                <div class="column"  v-if="result">
                    <div>
                        <h2 class="title ">Results</h2>
                        <hr>

                        <p ><strong>Car Check :  </strong > <span style="color:red; margin-left: 80px;">{{ Car.iscar ? "It is a car":"It is not a car"}}</span></p>
                        <hr>
                        <p ><strong>Damage Check :   </strong>  <span style="color:red; margin-left: 50px;">{{ Car.isdamaged ? "It is damaged":"It is not damaged  car" }}</span></p>
                        <hr>
                        <p ><strong>Location Check :  </strong> <span style="color:red; margin-left: 50px;">{{ Car.location }}</span></p>
                        <hr>
                        <p ><strong>Severity Check :  </strong> <span style="color:red; margin-left: 50px;"> {{ Car.severity }}</span></p>
                        <hr>
                        <div class="buttons">
                            <button class="button is-primary" @click="exportToPDF" >Create a PDF report and send to Vendor</button>
                            <button class="button is-link">Proceed to cost estimation </button>
                        </div>

                    </div>

                    <!-- <div v-else>


                        <div v-if="up_car" class="control">
                            <img src="require('assets/logo.png')" alt=" ">
                        </div> -->


                    <!-- </div> -->

                </div>
            </div>

        </div>
    </div>
</template>

<script>

import axios from 'axios'
import { toast } from 'bulma-toast'
import html2pdf from "html2pdf.js";

export default {
    name : 'Analysis',
    data(){
        return {
            Car: {},
            result : false,
            // up_car: false,
            loading : false

        }
    },
    mounted(){
        this.getCar()

    },

    methods : {
        async getCar(){
            const id = this.$route.params.id

           await axios
                .get(`/api/v1/car/${id}`)
                .then(response => {
                    this.Car = response.data

                })
                .catch(error =>{
                    console.log(error)
                })

        },

        async startanalysis(){

            const id = this.Car.id
            // this.up_car = true

            this.loading = true
           await axios
                .put(`/api/v1/engine/${id}`)
                .then(response => {
                    this.Car = response.data
                    this.result = true
                    // this.up_car = false
                    this.loading = false

                })
                .catch(error =>{
                    console.log(error)
                })

        },

        exportToPDF() {
            html2pdf(document.getElementById("element-to-convert"), {
				margin: 1,
                image:  { type: 'jpeg', quality: 0.98 },
  			    filename: "report.pdf",
                html2canvas:  { dpi: 192, letterRendering: true },
                jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
			});
        }

    }


}
</script>

<style>

    img{
        /* position:absolute; */
        height:350px;
        top:80px;
        left:500px;
        width:550px;
        border: #000000 6px outset
    }
</style>

