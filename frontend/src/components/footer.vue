<template>
    <div class="footer">
       <!-- Footer -->
            <footer class="page-footer font-small unique-color-dark pt-4">

            <!-- Footer Elements -->
            <div class="container">

                <!-- Call to action -->
                <ul class="list-unstyled list-inline text-center py-2">
                <li class="list-inline-item">
                    <h5 class="mb-1">Zarejestruj się i skorzystaj z naszych usług!</h5>
                </li>
                <li class="list-inline-item">
                    <a href="#!" class="btn btn-outline-secondary rounded-pill">Rejestracja</a>
                </li>
                </ul>
                <!-- Call to action -->

            </div>
            <!-- Footer Elements -->

            <!-- Copyright -->
            <div class="footer-copyright text-center py-3">© 2020 Copyright:
                <a href="https://github.com/MPorycki"> Marcin Porycki</a>
            </div>
            <!-- Copyright -->

            </footer>
            <!-- Footer -->
            </div>
</template>

<script>
import Menu from './menubar.vue'
export default {
    methods: {

    },
    mounted() {
        Menu.get_session()
        console.log("działa")
    }
}
</script>

<style scoped>
    .footer {
        background-color: #a4e6f4;
        width: 100%;
        height: wrap-content;
    }
    p {
        text-align: center;
        padding: 25px 0;
    }
    .footer-copyright {
        background-color: #6998a3;
        color: white;
    }

    .footer-copyright a {
        color: #f3bac3;
    }

</style>