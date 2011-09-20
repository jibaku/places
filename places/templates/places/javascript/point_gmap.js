{% load l10n %}
{% localize off %}
<script type="text/javascript">
    $(document).ready(function () {
        map = new google.maps.Map(document.getElementById('map_{{ name }}'), {
            zoom: {{ zoom_level }},
            zoomControl: true,
            zoomControlOptions: {
                style: google.maps.ZoomControlStyle.SMALL
            },
            center: new google.maps.LatLng({{ point.y }}, {{ point.x }}),
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var {{ name }}_marker = new google.maps.Marker({
            position:new google.maps.LatLng({{ point.y }}, {{ point.x }}),
            map: map,
            draggable: true
        });

        $('#id_{{ name }}')[0].value = "POINT(" + {{ name }}_marker.getPosition().lng() + " " + {{ name }}_marker.getPosition().lat() + ")";
        google.maps.event.addListener({{ name }}_marker, "dragend", function() {
            var point = {{ name }}_marker.getPosition();
            $('#id_{{ name }}')[0].value = "POINT(" + point.lng() + " " + point.lat() + ")";
        });
        $('#max_{{ name }}').click(function (event){
            event.preventDefault();
            var center = map.getCenter();
            $('#map_{{ name }}').width('{{ max_width }}px');
            $('#map_{{ name }}').height('{{ max_height }}px');
            google.maps.event.trigger(map, 'resize');  
            map.setCenter(center);
        });
        $('#min_{{ name }}').click(function (event){
            event.preventDefault();
            var center = map.getCenter();
            $('#map_{{ name }}').width('{{ min_width }}px');
            $('#map_{{ name }}').height('{{ min_height }}px');
            google.maps.event.trigger(map, 'resize');  
            map.setCenter(center);
        });
        
    });
</script>
{% endlocalize %}