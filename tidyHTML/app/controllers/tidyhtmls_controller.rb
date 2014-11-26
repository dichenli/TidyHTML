class TidyhtmlsController < ApplicationController
  #before_action :set_tidyhtml, only: [:show, :edit, :update, :destroy]
  PYNAME = "./app/assets/python/query.py"
  EMPTY_ORIGIN = ""
  EMPTY_CONVERT = ""
  TIDYHTML = "tidyHTML"
  FROM_STRING = "tidy_str"

  def convert
    @origin = tidyhtml_params[:origin]
    if @origin.nil? or @origin == ""
      @origin = EMPTY_ORIGIN
      @converted = EMPTY_CONVERT
    else
      @converted = converter(@origin) #convert a string stream of html to the tidy version
    end
    render action: 'main'
  end

  private
    # Never trust parameters from the scary internet, only allow the white list through.
    def tidyhtml_params
      params.permit(:origin) unless params.nil?
    end

    def converter(str)
      if str.nil?
        str = ''
      end
      File.open(PYNAME, 'wb'){|f| f.write "from #{TIDYHTML} import * \nprint #{FROM_STRING}(#{str.inspect})" }
      #File.open(PYNAME, 'wb'){|f| f.write "from #{TIDYHTML} import * \nprint #{FROM_STRING}(\"#{str.gsub(/\n/, '\\n')}\")" }
      #File.open(PYNAME, 'wb'){|f| f.write "from #{TIDYHTML} import * \nprint #{FROM_STRING}(\"#{str}\")" }
      return `python #{PYNAME}`
    end
end

#to do list:
#1. converter: generate a py query file that has random name, delete the file when query is done
#2. deal with \n, \t etc