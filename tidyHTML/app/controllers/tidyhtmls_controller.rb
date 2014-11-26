class TidyhtmlsController < ApplicationController
  #before_action :set_tidyhtml, only: [:show, :edit, :update, :destroy]
  PYNAME = "./app/assets/python/helloworld.py"
  EMPTY_ORIGIN = ""
  EMPTY_CONVERT = ""

  def convert
    @origin = tidyhtml_params[:origin]
    @converted = converter
    if @origin.nil? or @origin == ""
      @origin = EMPTY_ORIGIN
      @converted = EMPTY_CONVERT
    end
    render 'tidyhtmls/main'
  end

  private
    # Never trust parameters from the scary internet, only allow the white list through.
    def tidyhtml_params
      params.permit(:origin) unless params.nil?
    end

    def converter
      #File.open(PYNAME, 'r')
      return `python #{PYNAME}`
    end
end
