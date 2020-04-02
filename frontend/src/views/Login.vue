<template>
    <div class="container login-container" >
            <div class="row">
                <div class="col-md-6 login-form">
                    <h3>Logowanie</h3>
                    <form>
                        <div class="form-group">
                            <input type="text" id="login" class="form-control" placeholder="E-mail" value="" />
                        </div>
                        <div class="form-group">
                            <input type="password" id="password" class="form-control" placeholder="Hasło" value="" />
                        </div>
                        <div class="form-group">
                            <input type="submit" class="btnSubmit" value="Login" />
                        </div>
                        <div class="form-group">
                            <a href="#" class="ForgetPwd">Zapomniałeś hasła?</a>
                        </div>
                        <div class="form-group">
                            <a href="#" class="ForgetPwd">Nie masz konta?</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
</template>

<script>
import axios from 'axios'
import backend_url from "./variables"
export default {
    methods:{
        log_in(){
            var data = {
                login: document.getElementById("login").value,
                raw_password: document.getElementById("password").value
            }
            axios.post(backend_url  + "account/login", data).then(res => this.add_session_cookies(res.data["account_id"], res.data["session_id"]))
        },
    }
}
</script>

<style scoped>
    .login-container{
    margin-top: 5%;
    margin-bottom: 5%;
}
.login-form{
    padding: 5%;
    box-shadow: 0 5px 8px 0 rgba(0, 0, 0, 0.2), 0 9px 26px 0 rgba(0, 0, 0, 0.19);
    margin-left:25%;
}
.login-form-1 h3{
    text-align: center;
    color: #333;
}
.login-container form{
    padding: 10%;
}
.btnSubmit
{
    width: 50%;
    border-radius: 1rem;
    padding: 1.5%;
    border: none;
    cursor: pointer;
}
.btnSubmit{
    font-weight: 600;
    color: #6998a3;
    background-color: #a4e6f4;
}
.btnSubmit:hover{
    color: #fff;
    background-color: #f3bac3;
}
.ForgetPwd{
    color: #6998a3;
    font-weight: 600;
    text-decoration: none;
}
</style>