<template>
<div class="column is-4 is-offset-4">

    <h1 class="title">Pic a File</h1>
    
    <form @submit.prevent="submitForm" enctype="multipart/form-data">
            <div class="file  is-boxed is-success has-name">
                <label class="file-label">
                    <input class="file-input" type="file" name="resume"  @change="onFileChange">
                    <span class="file-cta">
                    <span class="file-icon">
                        <i class="fas fa-upload"></i>
                    </span>
                    <span class="file-label">
                        Pic a File
                    </span>
                    </span>
                    <span class="file-name">
                    Selected file : {{ this.Car.image ? this.Car.image.name : '' }}
                    </span>
                </label>
            </div>

            <div class="field" >
                    <div class="control mt-4">
                        <button type="submit" class="button is-link">Upload Your File</button>
                    </div>
            </div>

            <div class="control mt-4" v-if="this.Car.id">
             <router-link v-bind:to="Car.get_absolute_url" class="button is-dark"> Go to Analysis Page</router-link>
        </div>    
    </form>

          
</div>
</template>

<script>

import axios from 'axios'
import { toast } from 'bulma-toast'
export default {
    name : 'DetectionToolkit',
    data(){
        return{  
            Car : {
                id: 0,
                image: null,
                iscar: false,
                isdamaged: false,
                location: "",
                severity: "",
            },
               
        }
    },
    methods: {
        onFileChange(event){
            this.Car.image = event.target.files[0];
        },

        async submitForm(){
            let formData = new FormData();

            formData.append("image", this.Car.image);
        
            await axios
                .post('api/v1/upload/', formData
                )
                .then((res) => {
                        console.log(res);

                        this.Car = res.data

                        toast({
                            message: 'The Car was uploaded successfully. You can lauch the analysis now !!!',
                            type: 'is-info',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 4000,
                            position: 'top-center'
                        })         
                })
                .catch((error) => {
                        console.log(error);

                        toast({
                            message: 'An error occur. Are sure you have pic an image? ',
                            type: 'is-danger',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 4000,
                            position: 'top-center'
                        })
                });
            
        },
    },        
}
</script>