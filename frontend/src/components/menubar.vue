<template>
    <div class="header">
        <ul>
            <li><router-link to="/login" >Logowanie/Rejestracja</router-link></li>
            <li><router-link to="/" >Strona główna</router-link></li>
        </ul>
    </div>
</template>

<style scoped>
/*Paleta kolorow https://colorpalettes.net/color-palette-4182/ */
.header {
    background-color: #a4e6f4 ;
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
    color:#fff;
}

li:hover {
    display:block;
    background-color:#f3bac3;
}

.router-link-exact-active {
    background-color: #f3bac3;
    color: #fff;
}
</style>