from django import forms

<form method="POST" action="{% url 'create' %}" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="text" name="title">
    <input type="text" name="content">
    <input type="file" name="imgs" multiple>
    <input type="submit" value="작성하기">
</form>