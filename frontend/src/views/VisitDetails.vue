<template>
    <myForm>
        <H2>Szczegóły wizyty</H2>
        <button type="button" class="btn btn-danger" v-on:click="cancelVisit()">Odwołaj</button>
        <div id="fields" v-for="data in details" :key="data.id">
            <h5><strong>{{data.field_name}}</strong></h5>
            <p>{{data.field_value}}</p>
        </div>
    </myForm>
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
            id: ""
        }
    },
    mounted() {
        axios.get(this.$backend_url + "visit/"+this.$route.query.id).then(res => this.setDetails(res.data["details"]))
    },
    methods: {
        setDetails(detailsInput){
            for (var i=0; i < detailsInput.length; i++) {
                this.details.push(detailsInput[i])
            }
            this.id = this.$route.query.id
        },
        cancelVisit(){
            axios.delete(this.$backend_url + "visit/" + this.id).then(res => this.handleDeletionSuccess(res.data))
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
</style>