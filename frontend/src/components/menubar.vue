<template>
    <div class="header">
        <ul>
            <li v-if="this.session_id.length == 0">
                <router-link to="/login">Logowanie/Rejestracja</router-link>
            </li>
            <li v-else v-on:click="logout()">
                <a>Wyloguj</a>
            </li>
             <li>
                <router-link to="/allSalons">Salony</router-link>
            </li>
            <li>
                <router-link to="/visitsAll">Moje wizyty</router-link>
            </li>
            <li>
                <router-link to="/visitCreate">Umów się</router-link>
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
            user_id: "",
            session_id: ""
        }
    },
    methods: {
        get_session() {
            this.user_id = this.get_cookie("user-id")
            this.session_id = this.get_cookie("session-id")
        },
        get_cookie(cname) {
            var name = cname + "=";
            var decodedCookie = decodeURIComponent(document.cookie);
            var ca = decodedCookie.split(';');
            for (var i = 0; i < ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0) == ' ') {
                    c = c.substring(1);
                }
                if (c.indexOf(name) == 0) {
                    return c.substring(name.length, c.length);
                }
            }
            return "";
        },
        logout() {
            var data = { account_id: this.user_id, session_id: this.session_id }
            axios.delete(this.$backend_url + "account/logout", {data: data}).then(this.logout_success())
        },
        logout_success(){
            document.cookie = "session-id=;"
            document.cookie = "user-id=;"
            this.$router.push({ name: 'home', })
            this.get_session()
        },
        logout_failed(){
            alert("Wylogowanie nie powiodło się.")
        }

    },
    mounted() {
        this.get_session()
    }
}
</script>

<style scoped>
/*Paleta kolorow https://colorpalettes.net/color-palette-4182/ */

.header {
    background-color: #a4e6f4;
    height: 55px;
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
    background-color: #f3bac3;
}

.router-link-exact-active {
    background-color: #f3bac3;
    color: #fff;
}
</style>