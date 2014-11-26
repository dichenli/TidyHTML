require 'test_helper'

class TidyhtmlsControllerTest < ActionController::TestCase
  setup do
    @tidyhtml = tidyhtmls(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:tidyhtmls)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create tidyhtml" do
    assert_difference('Tidyhtml.count') do
      post :create, tidyhtml: { converted: @tidyhtml.converted, origin: @tidyhtml.origin }
    end

    assert_redirected_to tidyhtml_path(assigns(:tidyhtml))
  end

  test "should show tidyhtml" do
    get :show, id: @tidyhtml
    assert_response :success
  end

  test "should get edit" do
    get :edit, id: @tidyhtml
    assert_response :success
  end

  test "should update tidyhtml" do
    patch :update, id: @tidyhtml, tidyhtml: { converted: @tidyhtml.converted, origin: @tidyhtml.origin }
    assert_redirected_to tidyhtml_path(assigns(:tidyhtml))
  end

  test "should destroy tidyhtml" do
    assert_difference('Tidyhtml.count', -1) do
      delete :destroy, id: @tidyhtml
    end

    assert_redirected_to tidyhtmls_path
  end
end
