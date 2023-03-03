from flask import Flask, request, jsonify
import openai
from generateWebsite import generate_HTML_and_CSS
app = Flask(__name__)

@app.route("/")
def hello_world():
  return "hello_DeepDream"

# set up your OpenAI API key
openai.api_key = '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'

@app.route('/generate_logo', methods=['POST'])
def generate_logo():
    # get the prompt from the request
    prompt_raw = request.json['prompt']
    prompt = f"generate me a logo with that description {prompt_raw}"
    # create the image using OpenAI's Image API
    response = openai.Image.create(
        model="image-alpha-001",
        prompt=prompt,
        num_images=1)
    # get the image URL from the response
    image_url = response['data'][0]['url']
    # return the image URL as a JSON response
    return jsonify({'image_url': image_url})

@app.route('/generate_image', methods=['POST'])
def generate_image():
    # get the prompt from the request
    prompt_raw = request.json['prompt']
    prompt = f"""generate me an imafe that can be used for advertisment  with that description 
    {prompt_raw}"""
    # create the image using OpenAI's Image API
    response = openai.Image.create(
        model="image-alpha-001",
        prompt=prompt,
        num_images=1,
        size="1024x1024")
    # get the image URL from the response
    image_url = response['data'][0]['url']
    # return the image URL as a JSON response
    return jsonify({'image_url': image_url})
  
@app.route('/generate_ad_text' , methods=['POST'])
def generate_ad_text():
    # Get the prompt from the request
    prompt_raw = request.json['prompt']
    prompt = f"make an advertisment with a long pragraph  about this {prompt_raw}"
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    # Extract the generated text from the API response
    generated_text = response.choices[0].text
    # Return the generated text as a JSON response
    return jsonify({'generated_text': generated_text})


@app.route('/generate_video',methods=['POST'])
def generate_video(): 
  link ='https://hackathon-asset.s3.us-east-1.amazonaws.com/8752e3ba-4892-4b07-9a05-4da8219514f2%20%281%29.mp4?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBcaCXVzLXdlc3QtMSJGMEQCIFm73NZ2pnu1%2FIf%2F%2B7JewAYDRioAZV1E8fpeIPfeNQcxAiA%2FS9XdVBZoVldMZovRRkVANI0c5lniNm2V7O6RcfD8kCrtAgjA%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDY3NDM1MTM3MjgxOCIMAlsPBS4midDsB%2FRjKsEC0Ik6WrBDLWK2SA1P3fOWn2OS7UPkbASK45WjefDMpVwKlIGkJ8CcPWVVP7n5kEcImpfu0Ig2QKbXSkrPaVLHD1S9X640tzKTRNV5cduV0p%2F5oDQSUSwKc7WGLSlMtQaHi%2BBg33DwitWR73WC7gmppcLKBgicmpkp205j1uR5rtOrIJI72HbzAIIuEurLPv%2FdDCzIrFZoITwBszdMCqnokDX8KkXwi10xLnd7IZOwfBn4FcxcDiUjAuWdLpt8R3LPN1AVaIhwCO5Yp3oXaZs36H4imfThVnzTEbEgSPA8EIIzRWm5DJ8j%2B7S5AhmqXTTbqyI0WFadC5F%2BGjVRhtruKSR0plVdvClmOXUBHhwR6m0EiMz2Vt%2BsgaR5qA%2BkYGcJDp57ovxUmxU66%2BWRLflN00YwoO1kIbeQYVSdFzW8qScrMO2KiKAGOrQCIUzm4R1GQmdAxkhgbDU98VEpuAHiDjqekRduuAEv6Y6imThyGP9Czvr33QB467Rnhtlk825Lyb05LoOeM9VHQd1MwJWROLhxU9SdZqhbT%2BdgEr3rBK7jI%2FXIWwJ37KZGaUfurcQUdhZz0ZO6sUtW%2BjJuBlI%2BH0M%2BRsa%2BHhJGF%2FZdlXcyYHDkeyiMwhX%2FtgqiuUjLQpWblsbvNl3NxZQved6Mf0SC3Jg7pxKhHXJSElBeNfOmp6upywls%2B5k3C%2FvEvybPXcRkkSlDyllK0UqACce5t%2FkHWpG1X79CUt%2FIslDVMJOxfTRspNAsL9IykJ68P8Vxbx%2BQFWr9TEoP%2BnXkJWrGLV9b7arziQO8hXOMw%2BmwGXwDZdeqnOoU%2Bpk2sKAZKRcDLySX8Uy4luCdpxDxi0yOPaw%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230303T144708Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAZ2ATZLIJJ7OHQN6Z%2F20230303%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=fcb7c35aa7402ced09f5af5636bbc5bde4bc1d075246e9c4441bbf02e12745be'
  return jsonify({'generated_video': link})


@app.route('/generate_website' , methods=['POST'])
def generate_website():
    prompt = request.json['prompt']
    return generate_HTML_and_CSS(command=prompt)

if __name__ == "__main__" : 
  app.run(host='0.0.0.0', debug= True)
