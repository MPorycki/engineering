<template>
    <div class="header">
        <ul>
            <li v-if="this.sessionId == ''">
                <router-link to="/login">Logowanie/Rejestracja</router-link>
            </li>
            <div  v-else>
                <li v-on:click="logout()">
                    <a>Wyloguj</a>
                </li>
                <li>
                    <router-link :to="{ path: 'accountDetails', query: { id: this.userId }}">Konto</router-link>
                </li>
            </div>
            <li v-if="this.isAdmin == true">
               <a href="http://localhost:5000/admin/" target="_blank">Admin</a>
            </li>
            <li v-if="this.isHairdresser == true">
                <router-link to="/allCustomers">Klienci</router-link>
            </li>
            <li>
                <router-link to="/allSalons">Salony</router-link>
            </li>
            <li>
                <router-link to="/allServices">Usługi</router-link>
            </li>
            <li v-if="this.sessionId != ''">
                <router-link to="/visitsAll">Moje wizyty</router-link>
            </li>
            <li v-if="this.sessionId != '' && this.isHairdresser == false">
                <router-link to="/visitCreate">Umów się</router-link>
            </li>
            <li v-if="this.sessionId == ''" v-on:click="redirectToLogin()">
                <a>Umów się</a>
            </li>
            <li>
                <router-link to="/">Strona główna</router-link>
            </li>
        </ul>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            userId: "",
            sessionId: "",
            isAdmin: false,
            isHairdresser: false
        }
    },
    methods: {
        getSession(){
            var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
            axios.get(this.$backend_url + "session/", config).then(() => this.sessionStilValid()).catch(() => this.sessionInvalid())
        },
        sessionStilValid(){
            this.userId = this.$cookies.get('user-id')
            this.sessionId = this.$cookies.get('session-id')
            var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
            axios.get(this.$backend_url + "employee_access/", config).then(res => this.setAccess(res.data)).catch(() => this.handleAccessError())
        },
        setAccess(accessResults){
            this.isHairdresser = accessResults.isHairdresser
            this.isAdmin = accessResults.isAdmin
        },
        handleAccessError(){},
        sessionInvalid(){
            document.cookie = "session-id=;"
            document.cookie = "user-id=;"
        },
        logout() {
            var config = { headers: {account_id: this.$cookies.get('user-id'), session_id: this.$cookies.get('session-id')}}
            axios.delete(this.$backend_url + "account/logout", config).then(() => this.logoutSuccess()).catch(err => this.logoutFailed(err))
        },
        logoutSuccess(){
            document.cookie = "session-id=;"
            document.cookie = "user-id=;"
            this.$router.push({ name: 'home', })
            location.reload()
        },
        logoutFailed(err){
            if (err.response.status == 400){
                alert("Wylogowanie nie powiodło się.")
            } else {
                this.logoutSuccess()
            }
        },
        redirectToLogin(){
            this.$router.push({ name: 'Login', })
        }

    },
    mounted() {
        this.getSession()
    }
}
</script>

<style scoped>
/*Paleta kolorow https://colorpalettes.net/color-palette-4182/ */

.header {
    background-color: #a4e6f4;
    height: 56px;
    margin: 0;
    padding: 0;
    width: 100%;
}

ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
}

li {
    float: right;
    cursor: pointer
}

li a {
    display: block;
    text-align: center;
    padding: 16px;
    text-decoration: none;
    color: #6998a3;
}

a:hover {
    color: #fff;
}

li:hover {
    display: block;
    color: #fff;
    background-color: #f3bac3;
}

.router-link-exact-active {
    background-color: #f3bac3;
    color: #fff;
}
</style>