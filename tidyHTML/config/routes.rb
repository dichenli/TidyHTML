# == Route Map
#
#        Prefix Verb   URI Pattern                   Controller#Action
#     tidyhtmls GET    /tidyhtmls(.:format)          tidyhtmls#index
#               POST   /tidyhtmls(.:format)          tidyhtmls#create
#  new_tidyhtml GET    /tidyhtmls/new(.:format)      tidyhtmls#new
# edit_tidyhtml GET    /tidyhtmls/:id/edit(.:format) tidyhtmls#edit
#      tidyhtml GET    /tidyhtmls/:id(.:format)      tidyhtmls#show
#               PATCH  /tidyhtmls/:id(.:format)      tidyhtmls#update
#               PUT    /tidyhtmls/:id(.:format)      tidyhtmls#update
#               DELETE /tidyhtmls/:id(.:format)      tidyhtmls#destroy
#

Rails.application.routes.draw do
  post 'tidyhtmls/main', to: 'tidyhtmls#convert'
  root to: 'tidyhtmls#convert'
  #resources :tidyhtmls
  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".

  # You can have the root of your site routed with "root"
  # root 'welcome#index'

  # Example of regular route:
  #   get 'products/:id' => 'catalog#view'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

  # Example resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Example resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Example resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Example resource route with more complex sub-resources:
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', on: :collection
  #     end
  #   end

  # Example resource route with concerns:
  #   concern :toggleable do
  #     post 'toggle'
  #   end
  #   resources :posts, concerns: :toggleable
  #   resources :photos, concerns: :toggleable

  # Example resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end
end
