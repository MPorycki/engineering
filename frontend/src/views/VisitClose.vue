<template>
    <myForm>
        <h2>Podsumuj wizytę</h2>

        <form @submit.prevent="sendSummary">
            <div class="form-group">
                <input type="textbox" id="summary" class="form-control" placeholder="Notka" value="" />
                <b-tooltip target="summary" id="summary" class="rtooltips" triggers="hover" placement="right"  :disabled=true >{{email_text}}</b-tooltip>
            </div>
            <div class="form-group">
                <input type="file" id="pictureInput" class="form-control" placeholder="Obrazy" value="" />
                <b-tooltip target="password" id="password_error" class="rtooltips" triggers="hover" placement="right"  :disabled=true>{{password_text}}</b-tooltip>
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
            picture_ids: []
        }
    },
    mounted(){
        this.id = this.query.route.id
    },
    methods:{
        sendSummary(){
            var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
            var data = {"id": this.id, "summary": this.summary, "pictures": this.pictures}
            axios.patch(this.$backend_url + "visit/" + this.id, data, config)
        },
        onUpload(){
            this.picture=null;
            const storageRef=firebase.storage().ref(`${this.imageData.name}`).put(this.imageData);
            storageRef.on(`state_changed`,snapshot=>{
                this.uploadValue = (snapshot.bytesTransferred/snapshot.totalBytes)*100;
            }, error=>{console.log(error.message)},
            ()=>{this.uploadValue=100;
                storageRef.snapshot.ref.getDownloadURL().then((url)=>{
                this.picture =url;
                });
            }
            );
        }
    }
}
</script>

<style scoped>

</style>