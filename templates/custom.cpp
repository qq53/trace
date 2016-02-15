{% for c in calls -%}
void {{ c.name }}(int n){
{% if c.cond_str %}
	if ( {{ c.cond_str  }} ) {
		printf("{{ c.var_str }}\n", {{ c.value_str }});
	}
{% else %}
	printf("{{ c.var_str }}\n", {{ c.value_str }});
{% endif -%}
}
{% endfor -%}

void init_custom_call(){
#ifdef BIT32
	{% for c in calls_32 -%}
		syscall_trace[{{ c.upper() }}] = &{{ c }}_32;
	{% endfor %}
#else
	{% for c in calls_64 -%}
		syscall_trace[{{ c.upper() }}] = &{{ c }}_64;
	{% endfor %}
#endif
}
