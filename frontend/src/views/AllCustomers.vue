<template>
    <myForm>
        <h2>Klienci salonów Marco Polo</h2>
           <table class="col text-center" id="myTable" v-for="customer in customers" :key="customer.visit_id">
                <router-link tag="tr" id="tblrow" class="btn btn-light shadow" :to="{ path: 'accountDetails', query: { id: customer.id }}">
                    <p id="customerRow">
                        {{customer.firstName + " " + customer.lastName }}
                    </p>
                </router-link>
            </table>
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
            customers: []
        }
    },
    mounted(){
        var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
        axios.get(this.$backend_url + "account/", config).then(res => this.setCustomers(res.data["accounts"]))
    },
    methods: {
        setCustomers(customersInput){
            for (var i=0; i < customersInput.length; i++) {
                this.customers.push(customersInput[i])
            }
        }
    }
}
</script>

<style scoped>
    #myTable {
      margin-top: 25px;
      width: 50%;
      margin-left: auto;
      margin-right: auto;
    }

    #tblrow {
        height: 50px;
        width: 100%;
    }

    #customerRow{
        margin-top: 4%;
    }

</style>