<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_etymology_plugin import models %>
<%! active_menu_item = "cognatesets" %>

<h2>${_('Cognate sets')}</h2>
<div>
    ${ctx.render()}
</div>
