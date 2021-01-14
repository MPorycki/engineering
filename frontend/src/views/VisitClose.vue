<template>
    <myForm>
        <h2>Podsumuj wizytę</h2>

        <form @submit.prevent="sendSummary">
            <div class="form-group">
                <input type="textbox" id="summary" class="form-control" v-model="summary" placeholder="Notka" value="" />
            </div>
            <div class="form-group">
                <h4>Wgraj zdjęcia</h4>
                <input type="file" id="pictureInput" class="form-control" placeholder="Obrazy" value="" accept="image/x-png,image/gif,image/jpeg" v-on:change="this.onFileUpload"/>
            </div>
            <div class="form-group">
                <input type="submit" class="btnSubmit" value="Podsumuj" />
            </div>
        </form>
    </myForm>
</template>

<script>
import myForm from '../components/myForm'

import axios from 'axios'
import firebase from 'firebase'
export default {
    components: {
        myForm
    },
    data(){
        return {
            id: "",
            summary: "",
            picture: null
        }
    },
    mounted(){
        this.id = this.$route.query.id
    },
    methods:{
        sendSummary(){
            var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
            var ids = this.sendToFirebase();
            console.log(ids)
            var data = {"id": this.id, "summary": this.summary, "pictures": [ids]}
            axios.patch(this.$backend_url + "visit/" + this.id, data, config)
        },
        onFileUpload(event){
            var files = event.target.files
            this.picture = files
        },
        sendToFirebase(){
            var pictureIds;
            const storageRef=firebase.storage().ref(`${this.picture[0].name}`).put(this.picture[0]);
            storageRef.on(`state_changed`,snapshot=>{
                this.uploadValue = (snapshot.bytesTransferred/snapshot.totalBytes)*100;
            }, error=>{console.log(error.message)},
            ()=>{this.uploadValue=100;
                storageRef.snapshot.ref.getDownloadURL().then((url)=>{
                pictureIds =url;
                console.log(url)
                });
            }
            );
            return pictureIds;
        }
    }
}
</script>

<style scoped>
    #pictureInput{
        border: none;
    }
</style>