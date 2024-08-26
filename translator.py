import ezdxf

#Blot border dimensions
WIDTH = 125
HEIGHT = 125

def log(obj,iteration,coordinates,entity_recognized):
    if entity_recognized:
        match obj:
            case "line":
                print("Processing entity "+str(iteration)+", Entity = "+obj+
                      " @ coordinates = "+str(coordinates[0])+","+str(coordinates[1]))
            case "polyline":
                print("\nProcessing entity "+str(iteration)+", Entity = "+obj)
                for coordinate in coordinates:
                    print("point at ", coordinate, end=' ')
    else:
        print("Attempted to process unrecognized entity "+str(obj)+" at iteration "+str(iteration)+", skipping")


def negate_negativity(float):
    if (0>float):
        return -float

    
def dxf_to_blot_code(dxf_filename,scale):
    print("\nFunction ran with filename "+dxf_filename+"\n")
    file = ezdxf.readfile(dxf_filename)
    blot_code = [] #Blot code gets compiled here

    dxfmodel = file.modelspace() #Readability fun :)
    i = 0
    center_x = WIDTH / 2
    center_y = HEIGHT / 2
    
    for entity in dxfmodel: #Pull every entity from the model
        #TODO: Figure out why structured polygons aren't being represented as lines
        i += 1
        entity_type = entity.dxftype()
        if entity_type == 'LINE':

            start = entity.dxf.start
            end = entity.dxf.end
            
            startingpoint = [negate_negativity((round(start.x * scale - center_x, 2))), 
                             negate_negativity((round(start.y * scale - center_y, 2)))]
            
            endingpoint = [negate_negativity((round(end.x * scale - center_x, 2))), 
                           negate_negativity((round(end.y * scale - center_y, 2)))]
            
            polyline = [ #Define a STRAIGHT line by registering the coordinates of its start and endpoint
                startingpoint,
                endingpoint
            ]
            log("line",i,[startingpoint,endingpoint],True)
            blot_code.append(f'finalLines.push({polyline});')
            #An example polyline should look like [30,30], [-30, -30] uhh I gotta work on scale...
        if entity_type == 'POLYLINE' or entity_type == 'LWPOLYLINE':
            polyline = []
            
            for vertex in entity:
                point = [negate_negativity(round(vertex[0] * scale - center_x, 2)),
                         negate_negativity(round(vertex[1] * scale - center_y, 2))]
                polyline.append(point)
            
            log("polyline", i, polyline, True)
            blot_code.append(f'finalLines.push({polyline});')
        #todo-work on more entity types
        
        else:
            obj = entity_type
            log(obj,i,["?","?"],False) #If entity is unrecognized

    return blot_code

def main():
    filename = input("Enter filename: ")
    scale = float(input("Enter scale factor: "))
    blot_code = dxf_to_blot_code(filename+".dxf",scale)
    with open('output_blot.txt', 'w') as f:
        f.write("\n".join(blot_code))

if __name__ == "__main__":
    main()
    
