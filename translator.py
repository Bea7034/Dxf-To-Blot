import ezdxf

def dxf_to_blot_code(dxf_filename,scale):
    print("Function ran with filename "+dxf_filename)
    file = ezdxf.readfile(dxf_filename)
    blot_code = [] #Blot code gets compiled here

    dxfmodel = file.modelspace() #Readability fun :)

    for entity in dxfmodel: #Pull every object from the model
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            polyline = [ #Define a STRAIGHT line by registering the coordinates of its start and endpoint
                [round(start.x * scale, 2), round(start.y * scale, 2)],
                [round(end.x * scale, 2), round(end.y * scale, 2)]
            ]
            blot_code.append(f'finalLines.push({polyline});')
            #An example polyline should look like 0.9999999999999998, 0.9999999999999998 uhh I gotta work on scale...

        #todo-work on more entity types

    return blot_code

def main():
    filename = input("Enter filename: ")
    scale = float(input("Enter scale factor: "))
    blot_code = dxf_to_blot_code(filename+".dxf",scale)
    with open('output_blot.txt', 'w') as f:
        f.write("\n".join(blot_code))

main()

if __name__ == "__main__":
    main()
