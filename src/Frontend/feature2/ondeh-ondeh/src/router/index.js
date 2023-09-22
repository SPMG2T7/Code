import { createRouter, createWebHistory } from "vue-router";
import BrowsingRoles from "../components/views/staff/BrowseRolesListing.vue"
import CreateRoles from "../components/views/hr/RoleCreation.vue"

const routes = [
    {
        path: '/browseroles',
        name: "Browsing Roles",
        component: BrowsingRoles
    },
    {
        path: '/RoleCreation',
        name: "Creation of Roles",
        component: CreateRoles
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router