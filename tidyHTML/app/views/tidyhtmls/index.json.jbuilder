json.array!(@tidyhtmls) do |tidyhtml|
  json.extract! tidyhtml, :id, :origin, :converted
  json.url tidyhtml_url(tidyhtml, format: :json)
end
