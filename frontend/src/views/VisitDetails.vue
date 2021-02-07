<template>
    <div>
        <myForm>
            <H2>Szczegóły wizyty</H2>
            <div>
                <router-link v-if="this.summary == null" id="edit" :to="{ path: 'visitEdit', query: { id: this.id }}" class="btn btn-primary" >Edytuj</router-link>
                <router-link v-if="this.isHairdresser == true && this.summary == null" id="visitClose" :to="{ path: 'VisitClose', query: { id: this.id }}" class="btn btn-primary" >Zakończ</router-link>
                <router-link v-if="this.isHairdresser == true" id="customer" :to="{ path: 'AccountDetails', query: { id: this.customerId }}" class="btn btn-primary" >Klient</router-link>
            </div>
            <div id="fields" v-for="data in details" :key="data.id">
                <h5><strong>{{data.field_name}}</strong></h5>
                <p>{{data.field_value}}</p>
            </div>
        </myForm>
        <myForm v-if="this.summary != null">
            <H2>Podsumowanie</H2>
            <h5><strong>Notka</strong></h5>
            <p>{{this.summary.summary}}</p>
            <h5><strong>Zdjęcia</strong></h5>
            <div id="photos" v-for="photo in summary.pictures" :key="photo">
                <img id="photo" :src="photo" alt="">
            </div>
        </myForm>
    </div>
</template>

<script>
import myForm from '../components/myForm'

import axios from 'axios'
export default {
    components: {
        myForm
    },
    data(){
        return {
            details: [],
            summary: null,
            id: "",
            customerId: "",
            isHairdresser: false
        }
    },
    mounted() {
        var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
        axios.get(this.$backend_url + "visit/" + this.$route.query.id, config).then(res => this.setDetails(res.data))
        axios.get(this.$backend_url + "employee_access/", config).then(res => this.setAccess(res.data)).catch(() => this.handleAccessError())
    },
    methods: {
        setDetails(input){
            var detailsInput = input.details
            for (var i=0; i < detailsInput.length; i++) {
                this.details.push(detailsInput[i])
            }
            this.id = this.$route.query.id
            this.customerId = input.customerId
            if (Object.keys(input.summary).length > 0){
                this.summary = {}
                this.summary.summary = input.summary.summary
                this.summary.pictures = input.summary.pictures
                console.log(this.summary)
            }
        },
        setAccess(accessResults){
            this.isHairdresser = accessResults.isHairdresser
        },
        handleAccessError(){},
        cancelVisit(){
            var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
            axios.delete(this.$backend_url + "visit/" + this.id, config).then(res => this.handleDeletionSuccess(res.data))
        },
        handleDeletionSuccess(data){
            if (data){
                this.$router.push('/visitsAll')
            }
        }
    }
}
</script>

<style scoped>
    #fields{
        margin-top: 20px;
    }

    #edit, #customer, #visitClose{
        height: 40px;
        width: 100px;
        border: none;
        cursor: pointer;
        font-weight: 600;
        color: #6998a3;
        background-color: #a4e6f4;
        margin-right:25px;
    }

    #customer{
        margin-right: 0px;
    }
    #edit:hover, #customer:hover, #visitClose:hover{
        color: #fff;
        background-color: #f3bac3;
    }

    #photo{
        width: 75%;
        margin-top: 10px;
    }
</style>