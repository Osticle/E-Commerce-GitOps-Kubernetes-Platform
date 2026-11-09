{{/* Label for Service/Deployment choosing Pod. Will not be changed after deploy. */}}
{{- define "beeshoes.selectorLabels" -}}
app: {{ .Chart.Name }}
{{- end }}

{{/* metadata's Label for every resources */}}
{{- define "beeshoes.labels" -}}
{{ include "beeshoes.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version }}
{{- end }}
