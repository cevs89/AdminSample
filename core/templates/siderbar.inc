{% load static from staticfiles %}
<section>
    <!-- Left Sidebar -->
    <aside id="leftsidebar" class="sidebar">
        <!-- User Info -->
        <div class="user-info">
            <div class="image">
                <img src="{% static 'img/user.png' %}" width="48" height="48" alt="User" />
            </div>
            <div class="info-container">
                <div class="name" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Carlos Velazquz</div>
                <div class="email">carlos.velazquez@example.com</div>
                <div class="btn-group user-helper-dropdown">
                    <i class="material-icons" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">keyboard_arrow_down</i>
                    <ul class="dropdown-menu pull-right">
                        <li><a href="javascript:void(0);"><i class="material-icons">person</i>Profile</a></li>
                        <li role="separator" class="divider"></li>
                        <li><a href="javascript:void(0);"><i class="material-icons">group</i>Followers</a></li>
                        <li><a href="javascript:void(0);"><i class="material-icons">shopping_cart</i>Sales</a></li>
                        <li><a href="javascript:void(0);"><i class="material-icons">favorite</i>Likes</a></li>
                        <li role="separator" class="divider"></li>
                        <li><a href="javascript:void(0);"><i class="material-icons">input</i>Sign Out</a></li>
                    </ul>
                </div>
            </div>
        </div>
        <!-- #User Info -->
        <!-- Menu -->
        <div class="menu">
            <ul class="list">
                <li class="header">MAIN NAVIGATION</li>
                <li class="active">
                  <a href="/">
                    <i class="material-icons">home</i>
                    <span>Home</span>
                  </a>
                </li>
                <li>
                  <a href="javascript:void(0);" class="menu-toggle">
                      <i class="material-icons">assignment</i>
                      <span>knowledge</span>
                  </a>
                  <ul class="ml-menu">
                    <li>
                      <a href="{% url 'list_know' %}">List</a>
                    </li>
                    <li>
                      <a href="{% url 'create_know' %}">Create</a>
                    </li>
                  </ul>
                </li>
                <li>
                  <a href="javascript:void(0);" class="menu-toggle">
                      <i class="material-icons">assignment</i>
                      <span>Recognition</span>
                  </a>
                  <ul class="ml-menu">
                    <li>
                      <a href="{% url 'list_recon' %}">List</a>
                    </li>
                    <li>
                      <a href="{% url 'create_recon' %}">Create</a>
                    </li>
                  </ul>
                </li>
                <li>
                  <a href="javascript:void(0);" class="menu-toggle">
                      <i class="material-icons">assignment</i>
                      <span>Surveys</span>
                  </a>
                  <ul class="ml-menu">
                    <li>
                      <a href="{% url 'list_survey' %}">List Surveys</a>
                    </li>
                    <li>
                      <a href="{% url 'create_survey' %}">Create Surveys</a>
                    </li>
                  </ul>
                </li>

                <li>
                    <a href="{% url 'upload_csv' %}">
                        <i class="material-icons">assignment</i>
                        <span>Upload CSV</span>
                    </a>
                </li>

            </ul>
        </div>
        <!-- #Menu -->
        <!-- Footer -->
        <div class="legal">
            <div class="copyright">
                &copy; 2019 <a href="javascript:void(0);">KnowledgeBase - Material Design</a>.
            </div>
            <div class="version">
                <b>Version: </b> 1.0.5
            </div>
        </div>
        <!-- #Footer -->
    </aside>
    <!-- #END# Left Sidebar -->
</section>
