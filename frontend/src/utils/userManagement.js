
class UserManagementUtils {
    constructor (){}

    static getSession() {
        var userId = UserManagementUtils.getCookie("user-id")
        var sessionId = UserManagementUtils.getCookie("session-id")
        return {"userId":userId , "sessionId": sessionId}
    }

    static getCookie(cname) {
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
    }
}

export default UserManagementUtils