<template>
    <!-- START OF REFERENCE NAVBAR -->
    <!-- <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Navbar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">


                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                            aria-expanded="false">
                            Dropdown
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#">Action</a></li>
                            <li><a class="dropdown-item" href="#">Another action</a></li>
                            <li>
                                <hr class="dropdown-divider">
                            </li>
                            <li><a class="dropdown-item" href="#">Something else here</a></li>
                        </ul>
                    </li>

                </ul>
                <form class="d-flex" role="search">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav> -->
    <!-- END OF REFERENCE NAV BAR -->

    <nav class="navbar navbar-expand-lg bg-body-tertiary rounded-3">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">GoJobs Portal</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item profile-name">
                        <!-- Welcome, {{ name }} ({{ balance_points }} Points) -->
                        Welcome, Jeffry Tan!
                    </li>

                    <div class="nav-link p-0" data-bs-toggle="dropdown">
                        <li class="nav-item">
                            <button id="imgButton" class="btn btn-default">
                                <img src="../../assets/profile.jpeg" />
                            </button>


                            <div class="dropdown-menu dropdown-menu-end">
                        <!-- <li v-if="this.cid == 9999 || this.cid == 9998" @click="generateCharts">
                            <a class="dropdown-item">Dashboard</a>
                        </li> -->
                        <li><a class="dropdown-item">Settings</a>
                        </li>

                        <!-- LOG OUT BUTTON -->
                        <!-- <div class="dropdown-divider"></div>
                                <li @click="logout">
                                    <a class="dropdown-item"> Log Out</a>
                                </li> -->
                    </div>

                    </li>
            </div>
            </ul>
        </div>
        </div>
    </nav>
</template>

<style>
nav {
    background: linear-gradient(263deg, #946282 0%, #8BC100 100%);
}

.navbar-nav {
    display: flex;
    align-items: center;
    justify-content: center;
}

#imgButton {
    font-size: 24px;
    border: none;
    cursor: pointer;
    outline: none;
    margin: auto;
    display: block;
    background-color: transparent !important;
}

#imgButton:hover {
    background-color: transparent !important;
}

*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    position: relative;
    font-weight: normal;
}

img {
    width: 35px;
    height: 35px;
    object-fit: cover;
    border-radius: 50%;
}

.profile-name {
    color: white;
    font-weight: bold;
}

</style>